from copy import copy 
import signal
from threading import Lock, Thread
import sys 
from time import sleep
import logging

import Ice 

import icehms


class AgentManager(Thread):
    """ 
    Manage holons lifecycle.
    create an IceManager if necessary
    also takes care of catching signals 
    """
    def __init__(self, adapterId=None, catchSignals=True, daemon=False, icemgr=None, logLevel=logging.WARNING, defaultTimeout=500):
        """
        adapterID will be the Ice name of the adapter
        catchSginal will catch ctrl-C, this should only be done once per process.
        daemon will run main agentmanagerthread as daemon, this is necessary for atexit
        """
        Thread.__init__(self)

        if not adapterId:
            adapterId = Ice.generateUUID()

        self.logger = logging.getLogger(self.__class__.__name__ + "::" + self.getName())
        self.logger.setLevel(logLevel)
        if len(logging.root.handlers) == 0: #dirty hack
            logging.basicConfig(level=logging.DEBUG)
        self._shutdownEvent = False
        self._lock = Lock()
        self._agents = []
        if not icemgr:
            self.icemgr = icehms.IceManager(adapterId=adapterId, defaultTimeout=defaultTimeout)
        else:
            self.icemgr = icemgr
        self._stop = False
        self._agentsToRemove = []
        self._agentsToRemoveLock = Lock()

        if catchSignals:
            #Handle Ctrl-C on windows and linux
            signal.signal(signal.SIGINT, self.shutdown)
            signal.signal(signal.SIGTERM, self.shutdown)

        self._initializationFailed = False

        if daemon:
            self.setDaemon(1)

        self.logger.info("Starting")

        self.start()

        while not self.icemgr.initialized: # we need to make sure ice is initalized before anyone calls us
            if self._initializationFailed:
                self.logger.error( "Could not connect to Ice, is IceGrid running ? Exiting ...")
                sys.exit(1)
            sleep(0.01)


    def addAgent(self, agent, registerToGrid=False, daemon=False):
        """ Register an agent after the adapter has started
        """
        iceid = self.icemgr.ic.stringToIdentity(agent.name) #generate ID
        try:
            agent.proxy = self.icemgr.adapter.add(agent, iceid) #register holon
        except Ice.AlreadyRegisteredException:
            self.logger.warn( "Looks like you tried to register 2 times the same agent  : %s" % agent.name)
            return
        agent.proxy = self.icemgr.automatedCast(agent.proxy)
        agent.setAgentManager(self)
        if registerToGrid:
            self.icemgr.registerToIceGrid(agent)
            agent.registeredToGrid = True
        with self._lock:
            # keep list of agents for clean shutdown
            #might be possible to query icegrid adapter for that
            self._agents.append(agent)
        if daemon:
            agent.setDaemon(1)
        agent.start() #Start agent main thread

    def addHolon(self, holon, daemon=False):
        """
        same as addAgent but always register to IceGrid
        """
        self.addAgent(holon, registerToGrid=True, daemon=daemon)

    def removeAgent(self, agent):
        """
        De-register and shutdown an agent. 
        """
        with self._agentsToRemoveLock:
            self._agentsToRemove.append(agent)

    def removeHolon(self, agent):
        self.removeAgent(agent)

    def _removeAgent(self, agent):
        iceid = agent.proxy.ice_getIdentity()
        if agent.registeredToGrid:
            self.icemgr.deregisterToIceGrid(iceid) 
        self.icemgr.adapter.remove(iceid)
        self._agents.remove(agent)

    def isShutdown(self): 
        return self.icemgr.isShutdown()

    def waitForShutdown(self):
        return self.icemgr.waitForShutdown()

    def shutdown(self, sig=None, frame=None, join=True):
        """
        Clean shutdown
        stop thread and deregister/destroy Ice objects
        """
        self.logger.info( "Sending shutdown event" )
        self._shutdownEvent = True
        if join:
            self.join()

    def _shutdown(self):
        """
        Internal, called from agent mgr thread
        """
        self.logger.info( "Closing agent manager" )
        with self._lock:
            #send stop signal to all holons 
            for agent in self._agents: 
                self.logger.info( "sending stop to %s", agent.name )
                agent.stop() 
            # wait for holons to stop, if one is broken , we are dead ..
            for agent in copy(self._agents): 
                try:
                    self._shutdownAgent(agent)
                except (AttributeError, Ice.Exception) as why: #catch everything we must not fail
                    self.logger.warn("Error shuting down agent %s, %s", agent.name, why )
        self.logger.info( "Now closing Ice" )
        self.icemgr.destroy()
        self.logger.info( "Ice closed" )


    def run(self):
        try:
            self.icemgr.init()
        except Ice.Exception as why:
            self._initializationFailed = True
            self.logger.error( why )
            self._shutdownEvent = True

        while True:
            if self._shutdownEvent:
                self._shutdown()
                self.logger.info("Finished !")
                return
            if self._agentsToRemove:
                with self._agentsToRemoveLock:
                    for agent in self._agentsToRemove:
                        try:
                            self._shutdownAgent(agent)
                        except Ice.Exception as why: #catch everything we must not fail
                            self.logger.warn( "Error shuting down agent %s: %s", agent, why )
                        self._agentsToRemove.remove(agent)
            sleep(0.1)

    def _shutdownAgent(self, agent):
        agent.stop() #might allready be called but that is fine
        if isinstance(agent, Thread):
            self.logger.info( "Waiting for agent %s to stop ..." % agent.name  )
            if agent.isAlive():
                agent.join(2) 
        agent.cleanup() # let agent cleanup itself

        if isinstance(agent, Thread) and agent.isAlive():
            self.logger.warn( "Failed to stop main thread for agent: ", agent.name)
        else:
            self.logger.info( "agent %s stopped" % agent.name )
        self._removeAgent(agent)


def startHolonStandalone(holon, registerToGrid=True, logLevel=logging.WARNING, defaultTimeout=500):
    """
    Helper function to start one agent or holon
    """
    manager = AgentManager(adapterId=holon.name+"_adapter", defaultTimeout=defaultTimeout, logLevel=logLevel)
    manager.addAgent(holon, registerToGrid)
    manager.waitForShutdown()



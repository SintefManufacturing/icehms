from __future__ import with_statement

from copy import copy 
import signal
from threading import Lock, Thread
import sys 
from time import sleep
#from optparse import OptionParser


import Ice 

from icehms.icemanager import IceManager


class AgentManager(Thread):
    """ Initialize Ice and register holons as servant to Ice registry
    also takes care of catching signals and exiting Ice
    """
    def __init__(self, adapterId=None, catchSignals=True, daemon=False, icemgr=None, logLevel=3):
        """
        adapterID will be the Ice name of the adapter
        catchSginal will catch ctrl-C, this should only be done once per process.
        daemon will run main agentmanagerthread as daemon, this is necessary for atexit
        """
        Thread.__init__(self)

        if not adapterId:
            adapterId = Ice.generateUUID()

        self.setName(self.__class__.__name__ + "::" + adapterId) #set thread name for debuggin

        self._logLevel = logLevel
        self._shutdownEvent = False
        self._lock = Lock()
        self._agents = []
        if not icemgr:
            self.icemgr = IceManager(adapterId=adapterId, logLevel=logLevel)
        else:
            self.icemgr = icemgr
        self._stop = False
        self._agentsToRemove = []
        self._agentsToRemoveLock = Lock()

        if catchSignals:
            #Handle Ctrl-C on windows and linux
            signal.signal(signal.SIGINT, self.shutdown)
            signal.signal(signal.SIGTERM, self.shutdown)

        self._iceInitialized = False
        self._initializationFailed = False

        if daemon:
            self.setDaemon(1)

        self._log("Starting", level=2)

        self.start()

        while not self._iceInitialized: # we need to make sure ice is initalized before anyone calls us
            if self._initializationFailed:
                self._log( "Could not connect to Ice, is IceGrid running ? Exiting ...", level=1)
                sys.exit(1)
            sleep(0.1)

    def _log(self, msg, level=6):
        """
        log to stdout 

        0 Emergency: system is unusable
        1 Alert: action must be taken immediately
        2 Critical: critical conditions
        3 Error: error conditions
        4 Warning: warning conditions
        5 Notice: normal but significant condition
        6 Informational: informational messages
        7 Debug: debug-level messages
 
        """
        if level <= self._logLevel:
            print(str(level) + ":" + Thread.getName(self) +" : " + msg)

    def _ilog(self, *args, **kwargs):
        """
        format everything to string before logging
        """
        msg = ""
        if kwargs.has_key("level"):
            level = kwargs["level"]
        else:
            level = 6
        for arg in args:
            msg += str(arg)
        self._log(msg, level)

    def addAgent(self, agent, registerToGrid=False, daemon=False):
        """ Register an agen after the adapter has started
        """
        iceid = self.icemgr.ic.stringToIdentity(agent.name) #generate ID
        try:
            agent.proxy = self.icemgr.adapter.add(agent, iceid) #register holon
        except Ice.AlreadyRegisteredException:
            self._log( "Looks like you tried to register 2 times the same agent  : %s" % agent.name, level=2)
            return
        agent.proxy = self.icemgr.automatedCast(agent.proxy)
        agent.setAgentManager(self)
        if registerToGrid:
            self.icemgr.registerToIceGrid(agent.proxy)
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
        De-register an agent. to be called by external threads who destroyed an agent themselv
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
        self._ilog( "Sending shutdown event" )
        self._shutdownEvent = True
        if join:
            self.join()

    def _shutdown(self):
        """
        Internal, called from agent mgr thread
        """

        self._ilog( "Closing agent manager" )
        with self._lock:
            #send stop signal to all holons 
            for agent in self._agents: 
                self._ilog( "sending stop to ", agent.name )
                agent.stop() 
            # wait for holons to stop, if one is broken , we are dead ..
            for agent in copy(self._agents): 
                try:
                    self._shutdownAgent(agent)
                except (AttributeError, Ice.Exception), why: #catch everything we must not fail
                    self._ilog( why )
        self._ilog( "Now closing Ice" )
        self.icemgr.destroy()
        self._ilog( "Ice closed" )


    def run(self):
        try:
            self.icemgr.initIce()
            self._iceInitialized = True
        except Ice.Exception, why:
            self._initializationFailed = True
            self._ilog( why , level=1)
            self._shutdownEvent = True

        while True:
            if self._shutdownEvent:
                self._shutdown()
                self._log("Finished !", level=2)
                return
            if self._agentsToRemove:
                with self._agentsToRemoveLock:
                    for agent in self._agentsToRemove:
                        try:
                            self._shutdownAgent(agent)
                        except Ice.Exception, why: #catch everything we must not fail
                            self._ilog( why, level=3 )
                        self._agentsToRemove.remove(agent)
            if not sleep:
                self._ilog( "DEBUG: Sleep is None, ", self._shutdownEvent )
            sleep(0.1)

    def _shutdownAgent(self, agent):
        agent.stop() #might allready be called but that is fine
        self._ilog( "Waiting for agent %s to stop ..." % agent.name  )
        agent.join(2) 
        agent.cleanup() # remove personal topics for example

        if agent.isAlive():
            self._ilog( "Failed to stop main thread for agent: ", agent.name , level=1)
        else:
            self._ilog( "agent %s stopped" % agent.name , level=1 )
        self._removeAgent(agent)
 


def startHolonStandalone(holon, registerToGrid=True, logLevel=None, parseCmdLine=True):
    """
    Helper function to start one agent or holon
    """
    """
    if parseCmdLine:
        parser = OptionParser()
        parser.add_option("-v","--verbose", action="store", type="int", dest="logLevel")
    
        (options, args) = parser.parse_args()
        if options.logLevel != None:
            logLevel = options.logLevel
    """
    if logLevel != None:
        holon.setLogLevel(logLevel)
        manager = AgentManager(adapterId=holon.name+"_adapter", logLevel=logLevel)
    else:
        manager = AgentManager(adapterId=holon.name+"_adapter")
    manager.addAgent(holon, registerToGrid)
    manager.waitForShutdown()



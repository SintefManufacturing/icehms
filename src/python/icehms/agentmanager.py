"""
AgentManager
"""
import signal
from threading import Lock, Thread
import logging

import Ice 

import icehms


class AgentManager(object):
    """ 
    Manage holons lifecycle.
    create an IceManager if necessary
    also takes care of catching signals 
    """
    def __init__(self, adapterId=None, catchSignals=True, icemgr=None, logLevel=logging.WARNING, defaultTimeout=500):
        """
        adapterID will be the Ice name of the adapter
        catchSginal will catch ctrl-C, this should only be done once per process.
        """
        if not adapterId:
            adapterId = Ice.generateUUID()
        self.logger = logging.getLogger(self.__class__.__name__ + "::" + adapterId)
        if len(logging.root.handlers) == 0: #dirty hack
            logging.basicConfig()
        self.logger.setLevel(logLevel)
        self._agents = []
        self._lock = Lock()
        if not icemgr:
            self.icemgr = icehms.IceManager(adapterId=adapterId, defaultTimeout=defaultTimeout, logLevel=logLevel)
            self.icemgr.init()
        else:
            self.icemgr = icemgr

        if catchSignals:
            #Handle Ctrl-C on windows and linux
            signal.signal(signal.SIGINT, self.shutdown)
            signal.signal(signal.SIGTERM, self.shutdown)

    def add_agent(self, agent, registerToGrid=False, daemon=False):
        """ Register an agent after the adapter has started
        """
        with self._lock:
            iceid = self.icemgr.ic.stringToIdentity(agent.name) #generate ID
            try:
                agent.proxy = self.icemgr.adapter.add(agent, iceid) #register holon
            except Ice.AlreadyRegisteredException:
                self.logger.warn( "Looks like you tried to register 2 times the same agent  : %s" % agent.name)
                return
            agent.proxy = self.icemgr.automated_cast(agent.proxy)
            agent.set_agent_manager(self)
            if registerToGrid:
                self.icemgr.register_to_IceGrid(agent)
            self._agents.append(agent)
            if daemon:
                agent.setDaemon(1)
            agent.start() #Start agent main thread

    def add_holon(self, holon, daemon=False):
        """
        same as add_agent but always register to IceGrid
        """
        self.add_agent(holon, registerToGrid=True, daemon=daemon)

    def remove_agent(self, agent):
        """
        De-register and shutdown an agent. 
        """
        with self._lock:
            try:
                self._remove_agent(agent)
            except Exception as ex: #catch everything we must not fail
                self.logger.warn( "Error shutting down agent %s: %s", agent, ex )

    def remove_holon(self, agent):
        self.remove_agent(agent)

    def _remove_agent(self, agent, stop=True):
        if stop:
            agent.stop() 
        if isinstance(agent, Thread):
            self.logger.info( "Waiting for agent %s to stop ..." % agent.name  )
            if agent.isAlive():
                agent.join(2) 
        agent.cleanup() # let agent cleanup itself
        if isinstance(agent, Thread) and agent.isAlive():
            self.logger.warn( "Failed to stop main thread for agent: %s", agent.name)
        else:
            self.logger.info( "agent %s stopped" % agent.name )
        iceid = agent.proxy.ice_getIdentity()
        if agent.registeredToGrid:
            self.icemgr.deregister_to_IceGrid(iceid) 
        self.icemgr.adapter.remove(iceid)
        self._agents.remove(agent)

    def is_shutdown(self): 
        return self.icemgr.is_shutdown()

    def wait_for_shutdown(self):
        return self.icemgr.wait_for_shutdown()

    def shutdown(self, sig=None, frame=None):
        """
        Clean shutdown
        stop thread and deregister/destroy Ice objects
        """
        self.logger.info( "Shutdown" )
        with self._lock:
            for agent in self._agents: #send stop signal to all holons 
                self.logger.info( "sending stop to %s", agent.name )
                agent.stop() 
            for agent in self._agents.copy():# now really stop them 
                try:
                    self._remove_agent(agent, stop=False)
                except Exception as ex: #catch everything we must not fail
                    self.logger.warn("Error shuting down agent %s, %s", agent.name, ex )
        self.icemgr.destroy()

def run_holon(holon, registerToIceGrid=True, logLevel=logging.WARNING, defaultTimeout=500):
    """
    Helper function to start one agent or holon
    """
    run_holons([holon], registerToIceGrid, logLevel, defaultTimeout)

def run_holons(holons, registerToIceGrid=True, logLevel=logging.WARNING, defaultTimeout=500):
    """
    Helper function to start holons
    """
    manager = AgentManager(adapterId=holons[0].name+"s_adapter", defaultTimeout=defaultTimeout, logLevel=logLevel)
    for holon in holons:
        manager.add_agent(holon, registerToIceGrid)
    manager.wait_for_shutdown()




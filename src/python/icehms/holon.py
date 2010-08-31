from threading import Thread, Lock
from copy import copy
from time import sleep, time
import uuid

import Ice 


from icehms import hms


class Logger(object):
    def __init__(self, logLevel=3):
        self._logLevel = logLevel
        self._stop = False
        self._logPub = None
        self._logFile = None
        self._logToFile = False
        self._logToStdout = True
        self._logToTopic = False

    def setLogLevel(self, level, ctx=True):
        """
        As name says
        """
        self._logLevel = level
 
    def enableLogToTopic(self, current=None):
        """
        Start logging to a topic
        """
        self._logToTopic = True
        self._logPub = self._getPublisher("Log:" + self.name, hms.LogMonitorPrx, permanentTopic=False)

    def disableLogToTopic(self, current=None):
        """
        Stop logging to a topic
        """
        self._logToTopic = False

    def _log(self, msg, level=6):
        """
        log to enabled channels 

        0 Emergency: system is unusable
        1 Alert: action must be taken immediately
        2 Critical: critical conditions
        3 Error: error conditions
        4 Warning: warning conditions
        5 Notice: normal but significant condition
        6 Informational: informational messages
        7 Debug: debug-level messages
        """
        if type(level) != int:
            self.__log("self._log called with wrong argument !!!", 1)
            level = 1
        if level <= self._logLevel:
            self.__log(msg, level)

    def log(self, *args):
        """
        keep backward compatibility
        """
        self._log("Call to deprecated method self.log, please use self._log")
        return self._log(*args)

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
            msg += " " + str(arg)
        self._log(msg, level)

    def __log(self, msg, level):
        """
        internal , used by logging functions
        """
        msg = str(level) + "::" + self.__class__.__name__ + "::" + self.name + ": " + str(msg)
        if self._logToStdout:
            print(msg)
        if self._logToTopic and self._logPub:
            try:
                self._logPub.appendLog(msg)
            except Ice.Exception:
                print "Exception when publishing to topic, check topic manager"
        if self._logToFile:
            self._logFile.write(msg + "\n")

    def enableLogToStdout(self, ctx=None):
        self._logToStdout = True

    def disableLogToStdout(self, ctx=None):
        self._logToStdout = False

    def enableLogToFile(self, ctx=None):
        if not self._logToFile:
            try:
                self._logFile = open("Trace_"+ self.name + "_" + str(time()) + ".txt", "w")
            except IOError, why:
                self._ilog("Error opening log file: ", why)
                return False
            self._logToFile = True
        return True

    def disableLogToFile(self, ctx=None):
        self._logToFile = False
 






class Agent(hms.Agent, Logger, Thread, hms.GenericEventInterface):
    """Abstract agent class
    to be inherited by all agent
    implements mainly lifecycle (start stop, methods) and logging
    """
    def __init__(self, name=None, logLevel=3):
        Thread.__init__(self)
        Logger.__init__(self)
        self._icemgr = None
        if not name:
            name = self.__class__.__name__ + "_" + str(uuid.uuid1())
        self.name = name
        self.registeredToGrid = False
        self._lock = Lock()
        self._agentMgr = None
        self.proxy = None
        self._publishedTopics = {} 
        self._subscribedTopics = {}
        self.mailbox = MessageQueue()

    def getName(self, ctx=None): # we override method from Thread but I guess it is fine
        return self.name

    def setAgentManager(self, mgr): 
        """
        Set agent manager object for a holon. keeping a pointer enable us create other holons 
        also keep a pointer to icemgr
        """
        self._agentMgr = mgr
        self._icemgr = mgr.icemgr

    def subscribeTopic(self, topicName):
        self._log("Call to deprecated method Holon.subscribeTopic, use Holon._subscribeTopic", 2)
        return self._subscribeTopic(topicName)

    def _subscribeEvent(self, topicName):
        self._subscribeTopic(topicName, server=self._icemgr.eventMgr)

    def _subscribeTopic(self, topicName, server=None):
        """
        subscribe ourself to a topic using safest ice tramsmition protocol
        The holon needs to inherit the topic proxy and implemented the topic methods
        """
        topic = self._icemgr.subscribeTopic(topicName, self.proxy.ice_twoway())
        self._subscribedTopics[topicName] = topic
        return topic

    def _subscribeTopicUDP(self, topicName):
        """
        subscribe ourself to a topic, using UDP
        The holon needs to inherit the topic proxy and implemented the topic methods
        """
        topic = self._icemgr.subscribeTopic(topicName, self.proxy.ice_datagram())
        self._subscribedTopics[topicName] = topic
        return topic

    def getPublisher(self, topicName, prxobj, permanentTopic=False):
        self._log("Call to deprecated method Holon.getPublisher, use Holon._getPublisher", 2)
        return self._getPublisher(topicName, prxobj, permanentTopic)

    def _getPublisher(self, topicName, prxobj, permanentTopic=True, server=None):
        """
        get a publisher object for a topic
        create it if it does not exist
        prxobj is the ice interface obj for the desired topic. This is necessary since topics have an interface
        if permanentTopic is False then we destroy it when we leave
        otherwise it stays
        if server is None then default server is used
        """
 
        pub = self._icemgr.getPublisher(topicName, prxobj, server=server)
        self._publishedTopics[topicName] = permanentTopic
        return  pub

    def _getEventPublisher(self, topicName):
        """
        Wrapper over getPublisher, for generic event interface
        """
        return self._getPublisher(topicName, hms.GenericEventInterfacePrx, permanentTopic=False, server=self._icemgr.eventMgr)

    def newEvent(self, name, stringList, icebytes):
        """
        Received event from GenericEventInterface
        """
        self._log(2, "Holon registered to topic, but newEvent method not overwritten")

    def unsubscribeTopic(self, name):
        self._log("Call to deprecated method Holon.unsubscribeTopic, use Holon._unsubscribeTopic", 2)
        return self._unsubscribeTopic(name)

    def _unsubscribeTopic(self, name):
        """
        As the name says. It is necessary to unsubscribe to topics before exiting to avoid exceptions
        and being able to re-subscribe without error next time
        """
        self._subscribedTopics[name].unsubscribe(self.proxy)
        del(self._subscribedTopics[name])

  
    def isRunning(self, current=None):
        """
        Return True if thread runnnig
        Since some agents do not need threads, it might return False even if everythig is fine
        """
        return self.isAlive()

    def run(self):
        """ To be implemented by active holons
        """
        pass

    def cleanup(self):
        """
        Remove stuff from the database
        not catching exceptions since it is not very important
        """
        for topic in self._subscribedTopics.keys():
            self._unsubscribeTopic(topic)
        for k, v in self._publishedTopics.items():
            if not v:
                topic = self._icemgr.getTopic(k, create=False)
                if topic:
                    #topic.destroy()
                    self._ilog("Topic destroying disabled since it can confused clients")
        if self._logToFile:
            self._logFile.close()

    def start(self, current=None):
        """ overrriden so that it can be called from ice
        maybe ice should call something else ....
        """
        self._log("Starting", level=2)
        Thread.start(self)
                
    def stop(self, current=None):
        """
        Attempt to stop processing thread
        """
        self._ilog("stop called ")
        self._stop = True

    def shutdown(self, ctx=None):
        """
        shutdown a holon, stop thread and deregister from icegrid and icestorm
        I am not sure it is a good idea, maybe it should be private
        """
        try:
            self._agentMgr.removeAgent(self)
        except Ice.Exception, why:
            self._ilog(why)
        

    def getPublishedTopics(self, current):
        """
        Return a list of all topics published by one agent
        """
        return self._publishedTopics.keys()


    def getProxy(self, name):
        self._log( "Call to deprecated method Holon.getProxy", 2)
        self._log( "Use IceManager.getProxy", 2)
        return self._icemgr.getHolon(name)
 
    def findAllObjectsByType(self, icetype):
        self.log( "Call to deprecated method Holon.findAllObjectsByType", 2)
        self.log( "Use IceManager.findHolons", 2)
        return self._icemgr.findHolons(icetype)
    
    def getProxyBlocking(self, name):
        self._log( "Call to deprecated method Holon.getProxyBlocking", 2)
        self._log( "Use Holon._getProxyBlocking", 2)
        return self._getProxyBlocking(name)

    def _getProxyBlocking(self, address):
        return self._getHolonBlocking(address)

    def _getHolonBlocking(self, address):
        """
        Attempt to connect a given holon ID
        block until we connect
        return none if interrupted by self._stop
        """
        self._ilog( "Trying to connect  to " + address)
        prx = None    
        while not prx:
            prx = self._icemgr.getProxy(address)
            sleep(0.1)
            if self._stop:
                return None
        self._ilog( "Got connection to ", address)
        return prx

    def printMsgQueue(self, ctx=None):
        for msg in self.mailbox.copy():
            print "%s" % msg.creationTime + ' receiving ' + msg.body

    
    def putMessage(self, msg, current=None):
        #is going to be called by other process/or threads so must be protected
        self._ilog(self.__class__.__name__ + " got Message " + msg.body)
        self.mailbox.append(msg)

    def getClassName(self, ctx=None):
        return self.__class__.__name__



class stateSaver(object):
    def saveState(self, ctx=None):
        """
        Let holon save their internal state before relocation 
        return a state object
        return False if state saving is not possible or not implemented
        """
        return False

    def restoreState(self, state):
        """
        Let holon restore their internal state after relocation
        """
        return False
    






class Holon(hms.Holon, Agent):
    """Abstract holon class
    to be inherited by all holons
    """

    def __init__(self, *args, **kw):
        Agent.__init__(self, *args, **kw)

    def getState(self, current=None):
        """ default implementation of a getState
        should be re-imlemented in all clients
        """
        ans = []
        for msg in self.mailbox.copy():
            ans.append(msg.body)
        return ans



class MessageQueue(object):
    def __init__(self):
        self.lock = Lock()
        self._list = []
        
    def append(self, msg):
        self.lock.acquire()    
        self._list.append(msg)
        self.lock.release()

    def remove(self, msg):
        self.lock.acquire()
        #print "LIST", self._list
        #print msg
        self._list.remove(msg)
        self.lock.release()


    def pop(self):
        self.lock.acquire()
        if len(self._list) > 0:
            msg = self._list.pop()
        else: 
            msg = None
        self.lock.release()
        return msg

    def copy(self):
        """ return a copy of the current mailbox
        usefull for, for example, iteration
        """
        self.lock.acquire()
        #copy =  deepcopy(self._list)
        #shallow copy should be enough since as long as we have 
        # a link to the message python gc should not delete it
        # and as long as we do not modify message in our mailbox
        listcopy =  copy(self._list) 
        self.lock.release()
        return listcopy

    def __getitem__(self, x):
        """ to support mailbox[idx]"""
        return self._list.__getitem__(x)
    
    def __repr__(self):
        """ what is printed when printing the maibox  """
        return self._list.__repr__()




"""
This file define the main holon classes
BaseHolon implement the minim methods necessary for communication with other holons
LightHolons adds helper methods to handle message, topics and events
Holon adds a main thread to LightHolon
"""

from threading import Thread, Lock
import collections
from copy import copy
from time import sleep, time
import uuid
import logging

import Ice 


from icehms import hms


class BaseHolon_(object):
    """
    Base holon only implementing registration to ice
    and some default methods called by AgentManager
    """
    def __init__(self, name=None, hmstype=None, logLevel=logging.WARNING):
        if not name:
            name = self.__class__.__name__ + "_" + str(uuid.uuid1())
        self.name = name
        self.logger = logging.getLogger(self.__class__.__name__ + ":" + self.name)
        self.logger.setLevel(logLevel)
        if len(logging.root.handlers) == 0: #dirty hack
            logging.basicConfig()
        self._icemgr = None
        self.registeredToGrid = False
        self._agentMgr = None
        self.proxy = None
        if not hmstype:
            hmstype = self.ice_id()
        self.hmstype = hmstype

    def getName(self, ctx=None): 
        return self.name

    def setAgentManager(self, mgr): 
        """
        Set agent manager object for a holon. keeping a pointer enable us create other holons 
        also keep a pointer to icemgr
        """
        self._agentMgr = mgr
        self._icemgr = mgr.icemgr

    def cleanup(self):
        """
        Call by agent manager when deregistering
        """

    def start(self, current=None):
        """ 
        Call by Agent manager after registering
        """
        self.logger.info("Starting" )
                
    def stop(self, current=None):
        """ 
        Call by agent manager before deregistering
        """
        self.logger.info("stop called ")


    def shutdown(self, ctx=None):
        """
        shutdown a holon, deregister from icegrid and icestorm and call stop() and cleanup on holon instances
        I read somewhere this should notbe available in a MAS, holons should only shutdown themselves
        """
        try:
            self._agentMgr.removeAgent(self)
        except Ice.Exception, why:
            self.logger.warn(why)

    def getClassName(self, ctx=None):
        return self.__class__.__name__

    def __str__(self):
        return "[Holon: %s] " % (self.name)

    def __repr__(self):
        return self.__str__()




class LightHolon_(BaseHolon_):
    """Base Class for non active Holons or holons setting up their own threads
    implements helper methods like to handle topics, messages and events 
    """
    def __init__(self, name=None, hmstype=None, logLevel=logging.WARNING):
        BaseHolon_.__init__(self, name, hmstype, logLevel)
        self._publishedTopics = {} 
        self._subscribedTopics = {}
        self.mailbox = collections.deque()


    def _subscribeEvent(self, topicName):
        self._subscribeTopic(topicName, server=self._icemgr.eventMgr)

    def _subscribeTopic(self, topicName, server=None):
        """
        subscribe ourself to a topic using safest ice tramsmition protocol
        The holon needs to inherit the topic proxy and implemented the topic methods
        """
        topic = self._icemgr.subscribeTopic(topicName, self.proxy.ice_twoway(), server=server)
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
        self._publishedTopics[topicName] = (server, permanentTopic)
        return  pub

    def _getEventPublisher(self, topicName):
        """
        Wrapper over getPublisher, for generic event interface
        """
        return self._getPublisher(topicName, hms.GenericEventInterfacePrx, permanentTopic=True, server=self._icemgr.eventMgr)

    def newEvent(self, name, arguments, icebytes):
        """
        Received event from GenericEventInterface
        """
        self.logger.warn("Holon registered to topic, but newEvent method not overwritten")


    def _unsubscribeTopic(self, name):
        """
        As the name says. It is necessary to unsubscribe to topics before exiting to avoid exceptions
        and being able to re-subscribe without error next time
        """
        self._subscribedTopics[name].unsubscribe(self.proxy)
        del(self._subscribedTopics[name])

    def cleanup(self):
        """
        Remove stuff from the database
        not catching exceptions since it is not very important
        """
        for topic in self._subscribedTopics.keys():
            self._unsubscribeTopic(topic)

        for k, v in self._publishedTopics.items():
            if not v[1]:
                topic = self._icemgr.getTopic(k, server=v[0], create=False)
                if topic:
                    #topic.destroy()
                    self.logger.info("Topic destroying disabled since it can confuse clients")

    def getPublishedTopics(self, current):
        """
        Return a list of all topics published by one agent
        """
        return self._publishedTopics.keys()

    def putMessage(self, msg, current=None):
        """
        Called by other holons
        """
        self.logger.debug("Received message: " + msg.body)
        self.mailbox.appendleft(msg)



class Holon_(LightHolon_, Thread):
    """
    Holon is the same as LightHolon but starts a thread automatically
    """
    def __init__(self, name=None, hmstype=None, logLevel=logging.WARNING):
        Thread.__init__(self)
        LightHolon_.__init__(self, name, hmstype, logLevel)
        self._stop = False
        self._lock = Lock()

    def start(self):
        """
        Re-implement because start exist in LightHolon
        """
        Thread.start(self)

    def stop(self, current=None):
        """
        Attempt to stop processing thread
        """
        self.logger.info("stop called ")
        self._stop = True

    def _getProxyBlocking(self, address):
        return self._getHolonBlocking(address)

    def _getHolonBlocking(self, address):
        """
        Attempt to connect a given holon ID
        block until we connect
        return none if interrupted by self._stop
        """
        self.logger.info( "Trying to connect  to " + address)
        prx = None    
        while not prx:
            prx = self._icemgr.getProxy(address)
            sleep(0.1)
            if self._stop:
                return None
        self.logger.info( "Got connection to %s", address)
        return prx

    def run(self):
        """ To be implemented by active holons
        """
        pass



class BaseHolon(BaseHolon_, hms.Holon):
    def __init__(self, *args, **kw):
        BaseHolon_.__init__(self, args, **kw)

class LightHolon(LightHolon_, hms.Holon, hms.GenericEventInterface):
    def __init__(self, *args, **kw):
        LightHolon_.__init__(self, *args, **kw)

class Holon(Holon_, hms.Holon, hms.GenericEventInterface):
    def __init__(self, *args, **kw):
        Holon_.__init__(self, *args, **kw)



class Agent(hms.Agent, hms.Holon, Holon_):
    """
    Some people prefere working with agents instead of Holons
    """
    def __init__(self, *args, **kw):
        Holon_.__init__(self, *args, **kw)

class Message(hms.Message):
    """
    Wrapper over the Ice Message definition, 
    """
    def __init__(self, *args, **kwargs):
        hms.Message.__init__(self, *args, **kwargs)
        self.createTime = time()

    def __setattr__(self, name, val):
        #format everything to string
        if name == "parameters" and val:
            val = [str(i) for i in val]
        elif name == "arguments" and val:
            #val = {k:str(v) for k,v in val.items()} # does not work with python < 2.6
            d = dict()
            for k, v in val.items():
                if v in ("None", None): 
                    v = ""
                d[k] = str(v)
            val = d
        return hms.Message.__setattr__(self, name, val)






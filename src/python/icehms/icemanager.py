"""
IceManager initializes Ice and implement all low level methods necessary to IceHMS
"""
import sys
import socket # to get ip address
import logging

import Ice 
import IceGrid
import IceStorm

import icehms 


class IceManager(object):
    """
    create connection to ice
    creates also usefull proxies and wrapper methods around Ice methods
    """
    def __init__(self, adapterId=None, defaultTimeout=500, endpoints=None, logLevel=logging.WARNING, publishedEndpoints=None):
        """
        No adapterId argument means no adapter is created
        it can currently only handle one adapter, but we may have
        to add support for several adapters....maybe
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logLevel)
        if len(logging.root.handlers) == 0: #dirty hack
            logging.basicConfig()
        self._defaultTimeout = defaultTimeout

        self._publishedEndpoints = publishedEndpoints
        self._endpoints = endpoints

        self.initialized = False
        self._adapterId = adapterId

        self._session = None
        self._admin = None

        self.adapter = None
        self.registry = None
        self.query = None
        self.ic = None
        self.topicMgr = None
        self.messageTopicMgr = None
        self.realtimeMgr = None
        
        #authentication is disable so whatever works
        self._adminUser = "foo"
        self._adminPasswd = "bar"


    def init(self, properties=None):
        """ Initiliaze Ice and keep proxy to many interesting ice objects
        properties is and IceProperties object which can be used to set Ice properties (see doc)
        properties = Ice.createProperties(sys.argv) 
        for example:
            prop.setProperty("Ice.ThreadPool.Server.SizeMax", "100000")
        Note: some properties are required by icehms and are arbitrarily set in this method
        """
        if self.initialized:
            self.logger.warn("IceManager is allready initialized")
            return

        if not properties:
            properties = Ice.createProperties(sys.argv) 
        #self.logger.critical("Using ice registry located at: %s ",  icehms.IceRegistryServer )
        print("IceHMS::IceManager: Using ice registry located at: {0} ".format(icehms.IceRegistryServer))

        # those could be in cfg file but setting them programmatically gives much more flexibility
        if self._adapterId:
            properties.setProperty("hms.AdapterId", self._adapterId)
            myIP = self._getIP_to_IceGrid()
            if myIP:
                myIP = " -h " + myIP
            properties.setProperty("hms.Endpoints", "tcp " + myIP + ":udp " + myIP)
        properties.setProperty("Ice.Default.Locator", "IceGrid/Locator:" + icehms.IceRegistryServer)
        properties.setProperty("Ice.ThreadPool.Server.Size", "5")
        properties.setProperty("Ice.ThreadPool.Server.SizeMax", "100000")
        properties.setProperty("Ice.ThreadPool.Client.Size", "5")
        properties.setProperty("Ice.ThreadPool.Client.SizeMax", "100000")
        if self._publishedEndpoints:
            self.logger.info( "setting published endpoints %s: ", self._publishedEndpoints)
            properties.setProperty("hms.PublishedEndpoints", self._publishedEndpoints)
        if self._endpoints:
            self.logger.info( "setting endpoints:  %s", self._endpoints)
            properties.setProperty("hms.Endpoints", self._endpoints)

        
        #All properties set, now initialize Ice and get communicator object
        iceid = Ice.InitializationData()
        iceid.properties = properties
        self.ic = Ice.initialize(sys.argv, iceid)
        if self._adapterId:
            #create the adapter object
            #hms is the name used in the properties, so we cannot 
            # change it without changing the ice properties
            self.adapter = self.ic.createObjectAdapter("hms")
            self.adapter.activate() # allow request

        #Those objects must be created after adapter has been activated
        self.query = IceGrid.QueryPrx.checkedCast(self.ic.stringToProxy("IceGrid/Query"))
        self.registry =  IceGrid.RegistryPrx.uncheckedCast(self.ic.stringToProxy("IceGrid/Registry"))
        try:
            self.topicMgr = IceStorm.TopicManagerPrx.checkedCast(self.ic.stringToProxy("IceStorm/TopicManager"))
            self.messageTopicMgr = IceStorm.TopicManagerPrx.checkedCast(self.ic.stringToProxy("EventServer/TopicManager"))
            self.realtimeMgr = IceStorm.TopicManagerPrx.checkedCast(self.ic.stringToProxy("RealTimeServer/TopicManager"))
        except Ice.NotRegisteredException:
            print("Exception : if we fail here it is proably because icestorm is not registered in node !!")
            print("run register_services.sh in icehms")
            self.ic.destroy()
            raise

        # if we are here initilization should have worked
        self.initialized = True

    def _getIP_to_IceGrid(self):
        """
        return IP address on interface where we found the IceGrid server
        This is tricky
        return 127.0.0.1 if IceGrid server is not known
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serv = icehms.IceRegistryServer.split()
        ip = None 
        for idx, val in enumerate(serv): 
            if val == "-h":
                ip = serv[idx + 1]
        if not ip : 
            return "" 
        s.connect((ip, 0))#opening a dummy socket on the icegrid server machine
        ip = s.getsockname()[0]
        self.logger.info( "Deduced local IP address is: %s", s.getsockname()[0])
        return s.getsockname()[0]
    
    def _initAdmin(self):
        self._session = self.registry.createAdminSession(self._adminUser, self._adminPasswd)
        return self._session.getAdmin()

    def get_admin(self):
        """
        this method is implemented to work around timeout
        of admin session
        """
        if not self._admin:
            return self._initAdmin()
        else:
            try:
                self._session.ice_ping()
                self._admin.ice_ping()
            except Ice.Exception:
                return self._initAdmin()
            return self._admin

    def automated_cast(self, prx):
        """
        get ice type from ice, parse string and cast to specific type
        This is very usefull to avoid having to cast correctly every proxy we get from Ice
        This contains a lot of python magic and when something breaks in IceHMS it is usually here...
        """
        prx = prx.ice_timeout(300) 
        try:
            prx.ice_ping()
        except Ice.Exception as why:
            self.logger.warn("Proxy could not be ping, proxy is dead or database need cleaning %s, %s", why, prx)
            return prx # prx is dead but maybe user wants to investigate it 
        try:
            prxobj = self._get_prxobj(prx) #Try to cast
        except (ImportError, KeyError) as ex:
            self.logger.info( "Coult not cast to %s, casting to Holon. Error was: %s %s", prx.ice_id(), ex.__repr__(), ex)
            prxobj = icehms.hms.HolonPrx#If we fail here we have an installation problem or a bug
        prx = prxobj.checkedCast(prx)
        prx = prx.ice_timeout(self._defaultTimeout) #set timeout since we changed it for pinging
        return prx

    def _get_prxobj(self, prx):
        """
        absolutely not understandable python magic I wrote several years ago, but it works...
        """
        tmp = None
        icetype = prx.ice_id()
        icetype = icetype.split("::")
        tmp  = __import__(icetype[1]) #The first identifier is a slice module to import
        for t in icetype[2:-1]:
            tmp = tmp.__dict__[t]
        return tmp.__dict__[icetype[-1] + "Prx"]

    def register_to_IceGrid(self, agent):
        """ register Agent to iceregistry so that it can be found by type and ID
        """
        self.logger.debug( "Registring: %s with type %s", agent, agent.hmstype)
        try:
            self.get_admin().addObjectWithType(agent.proxy, agent.hmstype)
            agent.registeredToGrid = True
            return True
        except (IceGrid.ObjectExistsException):
            self.get_admin().updateObject(agent.proxy)
            agent.registeredToGrid = True
            return True
        except Ice.Exception as why:
            self.logger.error( "Could not register holon to grid: %s", why)
            return False

    def deregister_to_IceGrid(self, iceid):
        """
        deregister ice object to ice grid, if you have registered an object,
        it is a good idea to deregister it using this method
        """
        try:
            self.get_admin().removeObject(iceid)
        except IceGrid.ObjectNotRegisteredException:
            self.logger.warn( "Holon was not registered in database" )
        except Ice.ObjectNotExistException as why:
            self.logger.warn( "Could not de-register holon, admin obejct is dead !!!! report !!, %s", why )
        else:
            self.logger.info( "Holon %s de-registered" % iceid.name )

    def get_proxy(self, name):
        return self.get_holon(name)

    def get_holon(self, name):
        """
        return a proxy object of an Ice Holon, knowing its name(==id)
        return None if not found
        """
        prx = None
        if self.query:
            prx = self.query.findObjectById(self.ic.stringToIdentity(name))
            if prx:
                prx = self.automated_cast(prx)
                if prx:
                    self.logger.info( "got proxy for %s", prx)
        return prx

    def find_holons_quick(self, icetype):
        """ simple wrapper around findAllObjectsByType from ice
        but cast proxies to lowest level inherited object before returng list
        type is a string like "::hms::agv::Localizer"
        """
        holons = self.query.findAllObjectsByType( icetype )
        newlist = []
        for holon in holons:
            try:
                holon.proxy.ice_ping()
            except Ice.Exception:
                self.get_admin().removeObject(holon.proxy.ice_getIdentity())# it is dead
            else:
                prx = self.automated_cast(holon.proxy)
                newlist.append(prx)
        return newlist

    def find_holons(self, icetype="::hms::Holon"):
        """
        more expensive version of find_holons
        returns all object which inherit the given type
        """
        objs = self.get_admin().getAllObjectInfos("*")
        holons = []
        for obj in objs:
            try:
                if obj.proxy.ice_isA(icetype):
                    holons.append(self.automated_cast(obj.proxy))
            except Ice.Exception as e:
                self.get_admin().removeObject(obj.proxy.ice_getIdentity())# it is dead
                self.logger.warn("%s seems dead: %s, deleting it from registry", obj.proxy, e)
        return holons
    findAllObjectsByType = find_holons
    find_holons_by_type = find_holons
    
    def get_topic(self, topicName, create=True, server=None):
        """
        return an ice topic object for name topicName
        if create is True(default) then create topic if it does not exist
        """
        if not server:
            server = self.topicMgr
        try:
            topic = server.retrieve(topicName)
        except Ice.Exception: #sometime we crash with strange error message so better catch everything
            if create:
                try:
                    topic = server.create(topicName)
                except IceStorm.TopicExists:
                    #maybe someone has created it in between so re-try without catching check 
                    # if we get an exception here we cannot do much more
                    topic = server.retrieve(topicName)
            else:
                raise
        return topic

    def get_all_topics(self, server=None):
        """ return a dict of existing topics on given topic server 
        if None the default topic supporting messages is used
        """
        if server is None:
            server = self.messageTopicMgr
        return self.messageTopicMgr.retrieveAll()

    def get_publisher(self, topicName, prxobj, server=None):
        """
        get a publisher object for a topic
        create it if it does not exist
        prxobj is the ice interface obj for the desired topic. This is necessary since topics have an interface
        if server is None, default server is used
        """
        self.logger.debug("getting publisher for %s with prx %s at server %s", topicName, prxobj, server)
        topic = self.get_topic(topicName, server=server)
        publisher = topic.getPublisher() # get twoways publisher for topic
        self.logger.info("Got publisher for %s", topicName)
        return  prxobj.uncheckedCast(publisher)

    def subscribe_topic(self, topicName, prx, server=None):
        """
        subscribe prx to a topic
        The object pointed by the proxy needs to inherit the topic proxy and implemented the topic methods
        """
        topic = self.get_topic(topicName, server=server)
        qos = {}
        qos["reliability"] = "" #"" and "ordered" are the only possibilities see doc
        qos["retryCount"] = "-1" #-1 means to never remove a dead subscriber from list 
        try:
            topic.subscribeAndGetPublisher(qos, prx) 
        except IceStorm.AlreadySubscribed:
            self.logger.info( "Allready subscribed to topic" )
        self.logger.info( "subscribed %s to topic %s", prx, topicName )
        return topic

    def destroy(self):
        if self.ic:
            self.ic.destroy()
    shutdown = destroy

    def wait_for_shutdown(self):
        if self.ic: # we might crash here, waitForShutdown crashes if we are allready down
            self.ic.waitForShutdown()

    def is_shutdown(self):
        if self.ic:
            return self.ic.isShutdown()
        else:
            return True

    def get_cleaner(self):
        return icehms.Cleaner(self)





import sys
import socket # to get ip address
import logging

import Ice 
import IceGrid
import IceStorm

import icehms 
from icehms import hms


class IceManager(object):
    """
    create connection to ice
    creates also usefull proxies and wrapper methods around Ice methods
    """
    def __init__(self, adapterId=None, defaultTimeout=500, endpoints=None, publishedEndpoints=None):
        """
        No adapterId argument means no adapter is created
        it can currently only handle one adapter, but we may have
        to add support for several adapters....maybe
        """
        self._logger = logging.getLogger(self.__class__.__name__)
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
        self.eventMgr = None
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
            return

        if not properties:
            properties = Ice.createProperties(sys.argv) 
        #self._logger.critical("Using ice registry located at: %s ",  icehms.IceRegistryServer )
        print("IceHMS::IceManager: Using ice registry located at: {} ".format(icehms.IceRegistryServer) )

        # those could be in cfg file but setting them programmatically gives much more flexibility
        if self._adapterId:
            properties.setProperty("hms.AdapterId", self._adapterId)
            myIP = self._getIPToIceGrid()
            if myIP:
                myIP = " -h " + myIP
            properties.setProperty("hms.Endpoints", "tcp " + myIP + ":udp " + myIP)
        properties.setProperty("Ice.Default.Locator", "IceGrid/Locator:" + icehms.IceRegistryServer)
        properties.setProperty("Ice.ThreadPool.Server.Size", "5")
        properties.setProperty("Ice.ThreadPool.Server.SizeMax", "100000")
        properties.setProperty("Ice.ThreadPool.Client.Size", "5")
        properties.setProperty("Ice.ThreadPool.Client.SizeMax", "100000")
        if self._publishedEndpoints:
            self._logger.info( "setting published endpoints %s: ", self._publishedEndpoints)
            properties.setProperty("hms.PublishedEndpoints", self._publishedEndpoints)
        if self._endpoints:
            self._logger.info( "setting endpoints:  %s", self._endpoints)
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
        self._session = self.registry.createAdminSession(self._adminUser, self._adminPasswd)
        self._admin  = self._session.getAdmin()
        try:
            self.topicMgr = IceStorm.TopicManagerPrx.checkedCast(self.ic.stringToProxy("IceStorm/TopicManager"))
            self.eventMgr = IceStorm.TopicManagerPrx.checkedCast(self.ic.stringToProxy("EventServer/TopicManager"))
            self.realtimeMgr = IceStorm.TopicManagerPrx.checkedCast(self.ic.stringToProxy("RealTimeServer/TopicManager"))
        except Ice.NotRegisteredException:
            print "Exception : if we fail here it is proably because icestorm is not registered in node !!"
            print "run register_services.sh in icehms"
            self.ic.destroy()
            raise

        # if we are here initilization should have worked
        self.initialized = True

    def _getIPToIceGrid(self):
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
        self._logger.info( "Deduced local IP address is: %s", s.getsockname()[0])
        return s.getsockname()[0]

    def __getattr__(self, key):
        """
        this method is implemented to work around timeout
        of admin session
        """
        if key == 'session':
            try:
                self._session.ice_ping()
            except Ice.Exception:
                self._session = self.registry.createAdminSession(self._adminUser, self._adminPasswd)
            return self._session
        elif key == 'admin':
            try:
                self._admin.ice_ping()
            except Ice.Exception:
                self._admin  = self.session.getAdmin()
            return self._admin
        else:
            raise AttributeError(key)

    def automatedCast(self, prx):
        """
        get ice type from ice, parse string and cast to specific type
        This is very usefull to avoid having to cast correctly every proxy we get from Ice
        This contains a lot of python magic and when something breaks ince IceHMS it is usually here...
        """
        prx = prx.ice_timeout(300) 
        debugPrx = prx
        try:
            prx.ice_ping()
        except Ice.Exception, why:
            self._logger.warn("Proxy could not be ping, proxy is dead or database need cleaning %s, %s", why, prx)
            return prx # prx is dead but maybe wants to investigate it 
        if not prx: #it seems checkedCast sometimes returns None if it cannot cast to agent
            self._logger.warn( "Could not cast an obj to an agent, this is not normal %s, %s", prx, debugPrx)
            return prx
        #ids = prx.ice_ids()
        tmp = None
        #ids.reverse()
        #print("ids are: ", ids)
        ids = [prx.ice_id()]
        for icetype in ids:
            icetype = icetype.split("::")
            try:
                tmp  = __import__(icetype[1]) #The first identifier is a slice module to import
            except (ImportError), ex:
                self._logger.warn( "Import of slice module % s failed for object %s, %s", icetype[1], icetype, ex)
                continue
            try:
                for t in icetype[2:-1]:
                    tmp = tmp.__dict__[t]
                tmp = tmp.__dict__[icetype[-1] + "Prx"]
            except (KeyError), ex:
                self._logger.warn( "Ice type % s not found for object %s, %s" ,  icetype, prx, ex)
            else:
                break
        if tmp:
            prx = tmp.checkedCast(prx)
        prx = prx.ice_timeout(self._defaultTimeout) #set timeout since we changed it for pinging
        return prx

    def registerToIceGrid(self, agent):
        """ register Agent to iceregistry so that it can be found by type and ID
        """
        try:
            self.admin.addObjectWithType(agent.proxy, agent.hmstype)
            return True
        except (IceGrid.ObjectExistsException), why:
            self.admin.updateObject(agent.proxy)
            return False
        except Ice.Exception, why:
            self._logger.error( "Could not register holon to grid: %s", why)
            return False

    def deregisterToIceGrid(self, iceid):
        """
        deregister ice object to ice grid, if you have registered an object,
        it is a good idea to deregister it using this method
        """
        try:
            self.admin.removeObject(iceid)
        except IceGrid.ObjectNotRegisteredException, why:
            self._logger.warn( "Holon was not registered in database" )
        except Ice.ObjectNotExistException, why:
            self._logger.warn( "Could not de-register holon, admin obejct is dead !!!! report !!, %s", why )
        else:
            self._logger.info( "Holon %s de-registered" % iceid.name )

    def getProxy(self, name):
        return self.getHolon(name)

    def getHolon(self, name):
        """
        return a proxy object of an Ice Holon, knowing its name(==id)
        return None if not found
        """
        prx = None
        if self.query:
            prx = self.query.findObjectById(self.ic.stringToIdentity(name))
            if prx:
                prx = self.automatedCast(prx)
                if prx:
                    self._logger.info( "got proxy for %s", prx)
        return prx

    def findAllObjectsByType(self, icetype):
        return self.findHolons(icetype)
    def findHolonsByType(self, icetype):
        return self.findHolons(icetype)
    def findHolons_quick(self, icetype):
        """ simple wrapper around findAllObjectsByType from ice
        but cast proxies to lowest level inherited object before returng list
        type is a string like "::hms::agv::Localizer"
        """
        holons = self.query.findAllObjectsByType( icetype )
        newlist = []
        for holon in holons:
            prx = self.automatedCast(holon)
            if prx:
                try:
                    prx.ice_ping()
                except Ice.Exception:
                    pass
                else:
                    newlist.append(prx)
        return newlist

    def findHolons(self, icetype="::hms::Holon"):
        """
        more expensive version of findHolons
        returns all object which inherit the given type
        """
        objs = self.admin.getAllObjectInfos("*")
        holons = []
        for obj in objs:
            try:
                if obj.proxy.ice_isA(icetype):
                    holons.append(self.automatedCast(obj.proxy))
            except Exception, why:
                self._logger.warn("%s seems dead: %s", obj.proxy, why)
        return holons
    
    def getTopic(self, topicName, create=True, server=None):
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

    def getPublisher(self, topicName, prxobj, server=None):
        """
        get a publisher object for a topic
        create it if it does not exist
        prxobj is the ice interface obj for the desired topic. This is necessary since topics have an interface
        if server is None, default server is used
        """
        topic = self.getTopic(topicName, server=server)
        publisher = topic.getPublisher() # get twoways publisher for topic
        self._logger.info("Got publisher for %s", topicName)
        return  prxobj.uncheckedCast(publisher)

    def getEventPublisher(self, topicName):
        return self.getPublisher(topicName, hms.GenericEventInterfacePrx, server=self.eventMgr)

    def subscribeTopic(self, topicName, prx, server=None):
        """
        subscribe prx to a topic
        The object pointed by the proxy needs to inherit the topic proxy and implemented the topic methods
        """
        topic = self.getTopic(topicName, server=server)
        qos = {}
        qos["reliability"] = "" #"" and "ordered" are the only possibilities see doc
        qos["retryCount"] = "-1" #-1 means to never remove a dead subscriber from list 
        try:
            topic.subscribeAndGetPublisher(qos, prx) 
        except IceStorm.AlreadySubscribed:
            self._logger.info( "Allready subscribed to topic" )
        self._logger.info( "subscribed %s to topic %s", prx, topicName )
        return topic

    def shutdown(self):
        self.destroy()
    def destroy(self):
        if self.ic:
            self.ic.destroy()

    def waitForShutdown(self):
        if self.ic: # we might crash here, waitForShutdown crashes if we are allready down
            self.ic.waitForShutdown()

    def isShutdown(self):
        if self.ic:
            return self.ic.isShutdown()
        else:
            return True





import sys
import socket # to get ip address
import Ice 
import IceGrid
import IceStorm

import icehms 


class IceManager(object):
    """
    create connection to ice
    creates also usefull proxies and wrapper methods around Ice methods
    """
    def __init__(self, adapterId=None, defaultTimeout=500, logLevel = 2):
        """
        No argument means no adapter is created
        it can currently only handle one adapter, but we may have
        to add support for several adapter....maybe
        """
        self._logLevel = logLevel

        self._defaultTimeout = defaultTimeout

        self.initialized = False
        self._adapterId = adapterId

        self._session = None
        self._admin = None

        self.adapter = None
        self.registry = None
        self.query = None
        self.ic = None
        self.topicMgr = None
        
        #authentication is disable so whatever works
        self._adminUser = "foo"
        self._adminPasswd = "bar"


    def initIce(self):
        """ Initiliaze Ice and keep proxy to many interesting ice objects
        """

        prop = Ice.createProperties(sys.argv) 

        # those could be in cfg file but setting them programmatically gives much more flexibility
        if self._adapterId:
            prop.setProperty("hms.AdapterId", self._adapterId)
            myIP = self._getIPToIceGrid()
            if myIP:
                myIP = " -h " + myIP
            prop.setProperty("hms.Endpoints", "tcp " + myIP)
        prop.setProperty("Ice.Default.Locator", "IceGrid/Locator:" + icehms.IceRegistryServer)
        prop.setProperty("Ice.ThreadPool.Server.Size", "5")
        prop.setProperty("Ice.ThreadPool.Server.SizeMax", "100000")
        prop.setProperty("Ice.ThreadPool.Client.Size", "5")
        prop.setProperty("Ice.ThreadPool.Client.SizeMax", "100000")
        
        #All properties set, now initialize Ice and get communicator object
        iceid = Ice.InitializationData()
        iceid.properties = prop
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
        s.connect((ip, 0))#opening a dummy socket to port 0 on icegrid server
        ip = s.getsockname()[0]
        self._ilog( "Deduced local IP address is: ", s.getsockname()[0])
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
        get ice type from ice, parse string and cast to specific type !
        """
        prx = prx.ice_timeout(300) 
        debugPrx = prx
        try:
            prx.ice_ping()
        except Ice.Exception, why:
            self._ilog("Proxy could not be ping, maybe proxy is dead, maybe clean database", why, prx )
            return None # no need to return a dead proxy
        if not prx: #it seems checkedCast sometimes returns None if it cannot cast to agent
            self._ilog( "Could not cast an obj to an agent, this is not normal", prx, debugPrx, level=3)
            return None
        icetype = prx.ice_id() 
        icetype = icetype.replace("::", "", 1)
        icetype = icetype.replace("::", ".")
        try:
            tmp = "prx = icehms." + icetype + "Prx.checkedCast(prx)"
            exec tmp 
        except NameError:
            self._ilog( "Error executing:  ", tmp, level=3)
        prx = prx.ice_timeout(self._defaultTimeout) #set timeout since we changed it for pinging
        return prx

    def registerToIceGrid(self, proxy):
        """ register Agent to iceregistry so that it can be found by type and ID
        """
        try:
            self.admin.addObjectWithType(proxy, proxy.ice_id())
            return True
        except (IceGrid.ObjectExistsException), why:
            self.admin.updateObject(proxy)
            return False
        except Ice.Exception, why:
            self._ilog( "Could not register holon to grid !!!!!!", why, level=3)
            return False

    def deregisterToIceGrid(self, iceid):
        """
        deregister ice object to ice grid, if you have registered an object,
        it is a good idea to deregister it using this method
        """
        try:
            self.admin.removeObject(iceid)
        except IceGrid.ObjectNotRegisteredException, why:
            self._ilog( "Holon was not registered in database" )
        except Ice.ObjectNotExistException, why:
            self._ilog( "Could not de-register holon, admin obejct is dead !!!! report !!", why )
        else:
            self._ilog( "Holon %s de-registered" % iceid.name )


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
            print(str(level) + ":" + self.__class__.__name__ +" : " + msg)

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
                    self._ilog( "got proxy for ", prx)
        return prx

    def findAllObjectsByType(self, icetype):
        return self.findHolons(icetype)
    def findHolonsByType(self, icetype):
        return self.findHolons(icetype)
    def findHolons(self, icetype):
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
    
    def getTopic(self, topicName, create=True):
        """
        return an ice topic object for name topicName
        if create is True(default) then create topic if it does not exist
        """
        try:
            topic = self.topicMgr.retrieve(topicName)
        except Ice.Exception: #sometime we crash with strange error message so better catch everything
            if create:
                try:
                    topic = self.topicMgr.create(topicName)
                except IceStorm.TopicExists:
                    #maybe someone has created it in between so re-try without catching check 
                    # if we get an exception here we cannot do much more
                    topic = self.topicMgr.retrieve(topicName)
            else:
                raise
        return topic

    def getPublisher(self, topicName, prxobj):
        """
        get a publisher object for a topic
        create it if it does not exist
        prxobj is the ice interface obj for the desired topic. This is necessary since topics have an interface
        """
        topic = self.getTopic(topicName)
        publisher = topic.getPublisher() # get twoways publisher for topic
        self._ilog("Got publisher for ", topicName)
        return  prxobj.uncheckedCast(publisher)
    
    def subscribeTopic(self, topicName, prx):
        """
        subscribe prx to a topic
        The object pointed by the proxy needs to inherit the topic proxy and implemented the topic methods
        """
        topic = self.getTopic(topicName)
        qos = {}
        qos["reliability"] = "" #"ordered" is the other possibility see doc
        qos["retryCount"] = -1
        try:
            topic.subscribe({}, prx.ice_oneway()) #
        except IceStorm.AlreadySubscribed:
            self._ilog( "Allready subscribed to topic" )
        self._ilog( "subscribed", prx, " to topic ", topicName )
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




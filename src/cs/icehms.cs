using System;
using System.Net;
using System.Net.Sockets;  //This is only used to find our current IP address
using System.Collections.Generic;

/*
 * IceHMS is small wrapper around ice to setup a multi-agent like system
*/

namespace icehms
{

    public class Robot : icehms.Holon, hms.GenericRobotOperations_
    { // THis is just an example class inheriting holon and implementing another interface
        public Robot(IceManager app, string name)
            : base(app, name, false)
        {
            register((Ice.Object)new hms.GenericRobotTie_(this));
        }

        public virtual double[] getl(Ice.Current current)
        {
            return new double[6];
        }
        public void set_csys(hms.CSYS csys, Ice.Current cur = null)
        {
        }
        public virtual double[] getj(Ice.Current current)
        {
            return new double[6];
        }
        public void movel(double[] pose, double a, double v, Ice.Current current)
        {
        }
        public void translate(double[] pose, double a, double v, Ice.Current current)
        {
        }
        public void orient(double[] pose, double a, double v, Ice.Current current)
        {
        }
        public void movej(double[] pose, double a, double v, Ice.Current current)
        {
        }
        public bool is_program_running(Ice.Current current)
        {
            return false;
        }

        public void set_digital_out(int nb, bool val, Ice.Current current) { }
        public void set_analog_out(int nb, bool val, Ice.Current current) { }
        public bool get_digital_input(int nb, Ice.Current current) { return false; }
        public bool get_analog_input(int nb, Ice.Current current) { return false; }
        public void set_tool(int tool, Ice.Current current) { }
        public void set_tcp(Double[] tcp, Ice.Current current) { }
        public void grasp(Ice.Current current) { } // commodity method 
        public void release(Ice.Current current) { }

    }




    public class Holon : hms.HolonOperations_
    {
        public string Name;      // The holon name avertised on the network. It mus be unique
        public Ice.ObjectPrx Proxy; // an Ice proxy to myself
        public IceManager IceApp; //a  link to IceApp to communicate with the rest of the world
        public Ice.Object Servant;
        protected log4net.ILog logger;


        public Holon(icehms.IceManager app, string name, bool activate = true)
        {
            //The name must be unique!!
            Name = name;
            IceApp = app;
            logger = log4net.LogManager.GetLogger(this.GetType().Name + "::" + Name);

            if (activate)
            {
                register((Ice.Object)new hms.HolonTie_(this));
            }
        }

        protected void register(Ice.Object servant, bool icegrid = true)
        {
            Servant = servant;
            //logger.Info("registering: " + Servant.ice_id());
            Proxy = IceApp.register(Name, Servant, icegrid);
        }

        public virtual void shutdown()
        {
            //This must be called before closing application!!
            logger.Info("shutdown!");
            IceApp.deregister(this);
        }

        public string get_name(Ice.Current current = null)
        {
            return Name;
        }

        public virtual void put_message(hms.Message message, Ice.Current current)
        {
            logger.Warn("We got a new message but method is not implemented ");
        }

        public virtual void log(string message)
        {
            Console.WriteLine("IceHMS: " + Name + ": " + message);
        }
    }


    public class IceManager
    {
        /*
        * IceApp faciliate communication with other agents in icehms network
        * Initialize Ice, offer links to necessary objects, offer methods for common actions
        * One class per process
        * It can be shared between threads. Class is thread safe
        */
        public IceGrid.QueryPrx Query;
        public IceStorm.TopicManagerPrx EventMgr;
        public Ice.Communicator Communicator;
        string IceGridHost;
        int IceGridPort;
        IceGrid.AdminPrx _Admin;
        IceGrid.AdminSessionPrx _Session;
        IceGrid.RegistryPrx _Registry;
        Ice.ObjectAdapter _Adapter;
        public string Name;
        private List<Ice.Identity> _ServantIds;
        log4net.ILog logger;


        public IceManager(string adapterName, string host, int port, bool catchSignals = true)
        {

            IceGridHost = host;
            IceGridPort = port;
            Name = adapterName;

            logger = log4net.LogManager.GetLogger(this.GetType().Name + "::" + Name);

            _ServantIds = new List<Ice.Identity>(); //keep track of servants for emergency cleanup
            string myIP = findLocalIPAddress();
            logger.Info("My IPAddress is: " + myIP);

            //initialize Ice
            Ice.Properties prop = Ice.Util.createProperties();
            prop.setProperty("hms.AdapterId", adapterName);
            prop.setProperty("hms.Endpoints", "tcp -h " + myIP + ":udp -h " + myIP);
            prop.setProperty("Ice.Default.Locator", "IceGrid/Locator:tcp -p " + IceGridPort + " -h " + IceGridHost);
            prop.setProperty("Ice.ThreadPool.Server.Size", "5");
            prop.setProperty("Ice.ThreadPool.Server.SizeMax", "100000");
            prop.setProperty("Ice.ThreadPool.Client.Size", "5");
            prop.setProperty("Ice.ThreadPool.Client.SizeMax", "100000");

            Ice.InitializationData iceidata = new Ice.InitializationData();
            iceidata.properties = prop;
            Communicator = Ice.Util.initialize(iceidata); // could add sys.argv
            try
            {
                _Adapter = Communicator.createObjectAdapter("hms");
                _Adapter.activate();
            }
            catch (Exception ex)
            {
                logger.Fatal("Network error, check configuration: " + ex);
                logger.Fatal("Endpoint(should be local machine): " + prop.getProperty("hms.Endpoints"));
                logger.Fatal("Locator (should be IceGrid Server): " + prop.getProperty("Ice.Default.Locator"));
                throw (ex); // we are dead anyway
            }
            //Now are we ready to communicate with others
            //getting usefull proxies

            try
            {
                // proxy to icegrid to register our vc devices
                Query = IceGrid.QueryPrxHelper.checkedCast(Communicator.stringToProxy("IceGrid/Query"));
                if (Query == null)
                {
                    logger.Error("invalid ICeGrid proxy");
                }
                // proxy to icestorm to publish events
                EventMgr = IceStorm.TopicManagerPrxHelper.checkedCast(Communicator.stringToProxy("EventServer/TopicManager"));
                if (EventMgr == null)
                {
                    logger.Error("invalid IceStorm proxy");
                }
                //these 2 objects are only needed to get the IceGrid admin object in order to register
                _Registry = IceGrid.RegistryPrxHelper.uncheckedCast(Communicator.stringToProxy("IceGrid/Registry"));
                updateIceGridAdmin();

            }
            catch (Ice.NotRegisteredException)
            {
                logger.Fatal("If we fail here it is probably because the Icebox objects are not registered");
            }
            catch (Exception e)
            {
                logger.Fatal("IceGrid Server not found!!!!!: " + e);
                throw (e);//without yellow page system, there is no need to start
            }
            if (catchSignals)
            {
                setupSignals();
            }

        }

        public void setupSignals()
        {
            //ok it does not really catch signals in the current version
            Console.TreatControlCAsInput = false;
            Console.CancelKeyPress += new ConsoleCancelEventHandler(consoleHandle);
            //args.Cancel = true;
        }

        private void consoleHandle(object sender, ConsoleCancelEventArgs args)
        {
            logger.Fatal("Emergency shutdown");
            shutdown();
        }

        public void shutdown()
        {
            //alway call this, Ice needs to be closed cleanly
            logger.Info("IceApp " + Name + " shutdown");
            foreach (Ice.Identity iceid in _ServantIds) // that least should be empty, but deregister them avoid corrupting db
            {
                //logger.Info("deregistering: " + iceid);
                _deregister(iceid);
            }
            if (Communicator != null)
            {
                Communicator.destroy();
            }
        }

        private string findLocalIPAddress()
        {
            // machines can have many interfaces, there is no way to be sure we will return the correct interface
            // but by opening a socket to IceGrid we know that, at least, 
            // we use an IP address that can communicate to IceGrid
            UdpClient udpClient = new UdpClient(0);
            try
            {
                udpClient.Connect(IceGridHost, 0);
            }
            catch (Exception e)
            {
                // If we get here we have network problem, so returning something is probably stupide
                logger.Error("Error determining IP address, returning 127.0.0.1: " + e);
                return "127.0.0.1";
            }
            System.Net.IPAddress address = ((System.Net.IPEndPoint)udpClient.Client.LocalEndPoint).Address;
            string test = address.ToString();
            return IPAddress.Parse(test).ToString();
        }



        private IceGrid.AdminPrx updateIceGridAdmin()
        {
            _Session = _Registry.createAdminSession("foo", "bar"); //authentication is disable so whatever works
            _Admin = _Session.getAdmin();
            return _Admin;
        }

        private IceGrid.AdminPrx getIceGridAdmin()
        {
            if (_Session == null || _Admin == null)
            {
                updateIceGridAdmin();
            }
            else
            {
                // the session goes in timeout so check it
                try
                {
                    _Session.ice_ping();
                }
                catch (Ice.Exception) //Session and admin objects have timeouts, maybe they should be closed after used
                {
                    updateIceGridAdmin();
                }
            }
            return _Admin;
        }

        public Ice.ObjectPrx register(string Name, Ice.Object servant, bool icegrid = true)
        {
            // register an object to local Ice adapter and yellowpage service (IceGrid)

            Ice.Identity iceid = Communicator.stringToIdentity(Name);
            logger.Info("Registering: " + Name);//+ " with ice_id: " + iceid.ToString());
            Ice.ObjectPrx proxy;
            try
            {
                proxy = _Adapter.add(servant, iceid);
            }
            catch (Ice.AlreadyRegisteredException ex)
            {
                logger.Error("The name of this holon: " + iceid.ToString() + " is allready used in local adapter");
                //maybe I could try to change name but there is probably something wrong
                throw (ex);
            }

            // It is very important to deregister objects before closing!!
            // Otherwise ghost links are created
            IceGrid.AdminPrx admin = getIceGridAdmin();
            try
            {
                admin.addObjectWithType(proxy, servant.ice_id());
            }
            catch (IceGrid.ObjectExistsException)
            {
                admin.updateObject(proxy);
            }
            _ServantIds.Add(iceid);
            return proxy;
        }

        public void deregister(Holon holon)
        {
            //remove from IceGrid and from local adapter
            //this must be called before closing!!
            //logger.Info("Deregistring holon: " + holon.getName());
            Ice.Identity iceid = holon.Proxy.ice_getIdentity();
            _deregister(iceid);
            _ServantIds.Remove(iceid);
        }

        public void _deregister(Ice.Identity iceid)
        {
            IceGrid.AdminPrx admin = getIceGridAdmin();
            try
            {
                admin.removeObject(iceid);
            }
            catch (Exception ex)
            {
                logger.Warn("Could not deregister holon from IceGrid: " + ex);
            }
            _Adapter.remove(iceid);
        }


        public void subscribeEvent(Holon holon, string topicName)
        {
            IceStorm.TopicPrx topic = getTopic(topicName);
            Dictionary<string, string> qos = new Dictionary<string, string>();
            qos["reliability"] = ""; //#"" and "ordered" are the only possibilities see doc
            qos["retryCount"] = "-1"; // #-1 means to never remove a dead subscriber from list 
            try
            {
                topic.subscribeAndGetPublisher(qos, holon.Proxy);
            }
            catch (IceStorm.AlreadySubscribed)
            {
                logger.Info("Allready subscribed to topic, that is ok");
            }
            logger.Info(holon.Proxy + " subscribed to " + topicName);
        }

        public IceStorm.TopicPrx getTopic(string topicName)
        {
            // Retrieve the topic
            IceStorm.TopicPrx topic;
            try
            {
                topic = EventMgr.retrieve(topicName);
            }
            catch (IceStorm.NoSuchTopic)
            {
                try
                {
                    topic = EventMgr.create(topicName);
                }
                catch (IceStorm.TopicExists)
                {
                    //maybe someone has created it inbetween so try again, otherwise raise exception
                    topic = EventMgr.retrieve(topicName);
                }
            }
            return topic;

        }

        public hms.MessageInterfacePrx getEventPublisher(string topicName)
        {
            // Get the topic's publisher object, using towways
            IceStorm.TopicPrx topic = getTopic(topicName);
            Ice.ObjectPrx publisher = topic.getPublisher();
            return hms.MessageInterfacePrxHelper.uncheckedCast(publisher);
        }

        public Ice.ObjectPrx[] findHolons(string type) //wraper arond findAllObjectByType for consistency with python icehms
        {
            return Query.findAllObjectsByType(type);
        }
        public Ice.ObjectPrx getHolon(string name)
        {
            return Query.findObjectById(Communicator.stringToIdentity(name));
        }
    }
}

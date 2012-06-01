using System;
using System.Net;
using System.Net.Sockets;  //This is only used to find our current IP address
using System.Collections.Generic;

/*
 * IceHMS is small wrapper around ice to setup a multi-agent like system
*/

namespace icehms
{

    public class Robot : icehms.Holon, hms.RobotMotionCommandOperations_
    { // THis is just an example class inheriting holon and implementing another interface
        public Robot(IceApp app, string name) : base(app, name, false)
        {
            register((Ice.Object) new hms.RobotMotionCommandTie_(this));
        }
        public virtual double[] getl(hms.RobotCoordinateSystem c, Ice.Current current){
            return new double[6];
        }
        public virtual double[] getj(Ice.Current current){
            return new double[6];
        }
        public virtual void movel(double[] pose, double a, double v, hms.RobotCoordinateSystem c, Ice.Current current)
        {
        }
        public virtual void movej(double[] pose, double a, double v, Ice.Current current)
        {
        }
    }
    



    public class Holon : hms.HolonOperations_
    {
        public string Name;      // The holon name avertised on the network. It mus be unique
        public Ice.ObjectPrx Proxy; // an Ice proxy to myself
        public IceApp IceApp; //a  link to IceApp to communicate with the rest of the world
        protected Ice.Object Servant;
        

        public Holon(icehms.IceApp app, string name, bool activate=true)
        {
            //The name must be unique!!
            Name = name;
            IceApp = app;
            if (activate)
            {
                register((Ice.Object) new hms.HolonTie_(this));
            }
        }

        protected void register(Ice.Object servant)
        {
            Servant = servant;
            log("registreing: " + Servant.ice_id());
            Proxy = IceApp.register(Name, Servant);
        }


        public virtual void shutdown()
        {
            //This must be called before closing application!!
            IceApp.deregister(this);
        }

        public string getName(Ice.Current current=null)
        {
            return Name;
        }

        public void putMessage(hms.Message message, Ice.Current current)
        {
            log("We got a new message: " + message);
        }

        public void log(string message)
        {
            Console.WriteLine("IceHMS: " + Name + ": " + message);
        }
    }


    public class IceApp
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


       public IceApp(string adapterName, string host, int port)
       {
           IceGridHost = host;
           IceGridPort = port;
           Name = adapterName;
           string myIP = findLocalIPAddress();
           log("My IPAddress is: " + myIP);

           //initialize Ice
           Ice.Properties prop = Ice.Util.createProperties();
           prop.setProperty("hms.AdapterId", adapterName);
           prop.setProperty("hms.Endpoints", "tcp -h " + myIP +":udp -h " + myIP);
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
               log("Network error, check configuration: " + ex);
               log("Endpoint(should be local machine): " + prop.getProperty("hms.Endpoints"));
               log("Locator (should be IceGrid Server): " + prop.getProperty("Ice.Default.Locator"));
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
                   log("invalid ICeGrid proxy");
               }
               // proxy to icestorm to publish events
               EventMgr = IceStorm.TopicManagerPrxHelper.checkedCast(Communicator.stringToProxy("EventServer/TopicManager"));
               if (EventMgr == null)
               {
                   log("invalid IceStorm proxy");
               }
               //these 2 objects are only needed to get the IceGrid admin object in order to register
               _Registry = IceGrid.RegistryPrxHelper.uncheckedCast(Communicator.stringToProxy("IceGrid/Registry"));
               updateIceGridAdmin();

           }
           catch (Ice.NotRegisteredException)
           {
               log("If we fail here it is probably because the Icebox objects are not registered");
           }
           catch (Exception e)
           {
               log("IceGrid Server not found!!!!!: " + e);
               throw (e);//without yellow page system, there is no need to start
           }


       }

       public void shutdown()
       {
           //alway call this, Ice needs to be closed cleanly
           if (Communicator != null)
           {
               Communicator.destroy();
           }
       }

       public void log(string message)
       {
           Console.WriteLine("IceHMS: " + message);
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
                log("Error determining IP address, returning 127.0.0.1: " + e);
                return "127.0.0.1";
            }
            System.Net.IPAddress address = ((System.Net.IPEndPoint)udpClient.Client.LocalEndPoint).Address;
            string test = address.ToString();
            return IPAddress.Parse(test).ToString() ;
       }



       private IceGrid.AdminPrx updateIceGridAdmin()
       {
           _Session = _Registry.createAdminSession("foo", "bar"); //authentication is disable so whatever works
           _Admin = _Session.getAdmin();
           return _Admin;
       }

       private IceGrid.AdminPrx getIceGridAdmin()
       {
           if (_Session == null || _Admin ==null)
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

       public Ice.ObjectPrx register(string Name, Ice.Object servant)
       {
            // register an object to local Ice adapter and yellowpage service (IceGrid)
            Ice.Identity iceid = Communicator.stringToIdentity(Name);
            Ice.ObjectPrx proxy;
            try
            {
                proxy = _Adapter.add(servant, iceid);
            }
            catch (Ice.AlreadyRegisteredException ex)
            {
                log("The name ArgumentOutOfRangeException this holon is allready used");
                //maybe I could try to change name but there is probably something wrong in modell
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
           return proxy;
       }

       public void deregister(Holon holon)
       {
            //remove from IceGrid and from local adapter
           //this must be called before closing!!
            Ice.Identity iceid = holon.Proxy.ice_getIdentity();
            IceGrid.AdminPrx admin = getIceGridAdmin();
            try
            {
                admin.removeObject(iceid);
            }
            catch (Exception ex)
            {
                log("Could not deregister holon from IceGrid: " + ex);
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
            log( "Allready subscribed to topic, that is ok" );
        }
        log(holon.Proxy + " subscribed to " + topicName );
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

       public hms.GenericEventInterfacePrx getEventPublisher(string topicName)
       {
           // Get the topic's publisher object, using towways
           IceStorm.TopicPrx topic = getTopic(topicName);
           Ice.ObjectPrx publisher = topic.getPublisher();
           return hms.GenericEventInterfacePrxHelper.uncheckedCast(publisher);
       }

       public Ice.ObjectPrx[] findHolon(string type) //wraper arond findAllObjectByType for consistency with python icehms
       {
           return Query.findAllObjectsByType(type);
       }
   }
}

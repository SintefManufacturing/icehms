using System;
//using hms; cleaner to says hms everytime

namespace icehms
{
   public class IceApp
   {
       IceGrid.QueryPrx m_query;
       IceStorm.TopicManagerPrx m_eventMgr;
       Ice.Communicator m_communicator;


       public IceApp()
       {

           //initialize Ice
           Ice.Properties prop = Ice.Util.createProperties();
           prop.setProperty("hms.AdapterId", "VC2ICE");
           //prop.setProperty("hms.Endpoints", "tcp -h SINTEFPC1671.sintef.no:udp -h sintefpc1671.sintef.no ");
           //prop.setProperty("Ice.Default.Locator", "IceGrid/Locator:tcp -p 12000 -h utopia.sintef.no");
           prop.setProperty("hms.Endpoints", "tcp -h SINTEFPC1671.sintef.no:udp -h localhost ");
           prop.setProperty("Ice.Default.Locator", "IceGrid/Locator:tcp -p 12000 -h localhost");
           prop.setProperty("Ice.ThreadPool.Server.Size", "5");
           prop.setProperty("Ice.ThreadPool.Server.SizeMax", "100000");
           prop.setProperty("Ice.ThreadPool.Client.Size", "5");
           prop.setProperty("Ice.ThreadPool.Client.SizeMax", "100000");

           Ice.InitializationData iceidata = new Ice.InitializationData();
           iceidata.properties = prop;
           m_communicator = Ice.Util.initialize(iceidata); // could add sys.argv

           try
           {
               // proxy to icegrid to register our vc devices
               m_query = IceGrid.QueryPrxHelper.checkedCast(m_communicator.stringToProxy("IceGrid/Query"));
               if (m_query == null)
               {
                   Console.WriteLine("invalid ICeGrid proxy");
               }
               // proxy to icestorm to publish events
               m_eventMgr = IceStorm.TopicManagerPrxHelper.checkedCast(m_communicator.stringToProxy("EventServer/TopicManager"));
               if (m_eventMgr == null)
               {
                   Console.WriteLine("invalid IceStorm proxy");
               }
           }
           catch (Ice.NotRegisteredException)
           {
               Console.WriteLine("If we fail here it is probably because the Icebox objects are not registered");
           }
           catch (Ice.NoEndpointException)
           {
               Console.WriteLine("IceGrid Server not found!!!!!");
           }
       }
       public void cleanup()
       {
           if (m_communicator != null)
           {
               m_communicator.destroy();
           }
       }

       public hms.GenericEventInterfacePrx getEventPublisher(string topicName)
       {
           // Retrieve the topic
           IceStorm.TopicPrx topic;
           try
           {
               topic = m_eventMgr.retrieve(topicName);
           }
           catch (IceStorm.NoSuchTopic)
           {
               try
               {
                   topic = m_eventMgr.create(topicName);
               }
               catch (IceStorm.TopicExists)
               {
                   //maybe someone has created it inbetween so try again, otherwise raise exception
                   topic = m_eventMgr.retrieve(topicName);
               }
           }
           // Get the topic's publisher object, using towways
           Ice.ObjectPrx publisher = topic.getPublisher();
           return hms.GenericEventInterfacePrxHelper.uncheckedCast(publisher);
       }
       public Ice.ObjectPrx[] findHolon(string type) //wraper arond findAllObjectByType for consistency with python icehms
       {
           return m_query.findAllObjectsByType(type);
       }
   }
}

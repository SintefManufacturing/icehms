 
using System;
using icehms;
using System.Threading;
 
class Test {
    static void Main() {
        Console.WriteLine ("Starting");

        IceApp app = null;
        try
        {
            //app = new IceApp("localhost", 12000);
            app = new IceApp("MyTestAdapter", "utopia.sintef.no", 12000);
            Holon holon = new Holon("MyTestHolon");
            Console.WriteLine(holon.Name + " starting");
            app.register(holon);
            app.subscribeEvent(holon, "MyTopic");
            hms.GenericEventInterfacePrx pub = app.getEventPublisher("MyTopic");
            Thread.Sleep(1000);
            hms.Message msg = new hms.Message() ;
            msg.arguments = new System.Collections.Generic.Dictionary<string, string>();
            msg.arguments.Add("mynewargs", "totoisback");
            pub.putMessage(msg);
            Thread.Sleep(1000);
            pub.putMessage(msg);
            Console.WriteLine ("Sleeping");
            Thread.Sleep(10000);
            Console.WriteLine ("Cleanup");
            app.deregister(holon);
        }
        finally
        {
            if ( app != null ) 
            {
                app.cleanup();
            }
        }
    }
}

 
using System;
using icehms;
using System.Threading;
 
class Test {
    static void Main() {
        Console.WriteLine ("Starting");

        IceApp app = null;
        Holon holon = null;
        try
        {
            app = new IceApp("MyTestAdapter", "localhost", 12000);
            holon = new Holon(app, "MyTestHolon");
            Console.WriteLine(holon.Name + " starting");
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
            
        }
        finally
        {
            if (holon != null )
            {
                holon.shutdown();
            }
            if ( app != null ) 
            {
                app.shutdown();
            }
        }
    }
}

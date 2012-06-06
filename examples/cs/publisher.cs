 
using System;
using icehms;
using System.Threading;
 
class Test {
    static void Main() {
        IceApp app = null;
        try
        {
            app = new IceApp("MyTestAdapter", "localhost", 12000);
            hms.GenericEventInterfacePrx pub = app.getEventPublisher("MyTopic");
            int count = 0;
            while ( true )
            {
                Thread.Sleep(1000);
                count++;
                hms.Message msg = new hms.Message() ;
                msg.arguments = new System.Collections.Generic.Dictionary<string, string>();
                msg.arguments.Add("Counter", count.ToString());
                msg.arguments.Add("arg1", "totoisback");
                msg.arguments.Add("arg2", "somethingnew");
                pub.putMessage(msg);
            }
            
        }
        finally
        {
            if ( app != null ) 
            {
                app.shutdown();
                Console.WriteLine("Stop 1");
            }
                Console.WriteLine("Stop 2");
        }
    }
}

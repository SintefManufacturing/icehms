 
using System;
using icehms;
using System.Threading;
 
class Test {
    static void Main() {
        Console.WriteLine ("Starting");

        IceApp app = null;
        try
        {
            app = new IceApp("localhost", 12000);
            Holon holon = new Holon("MyTestHolon");
            Console.WriteLine(holon.Name + " starting");
            app.register(holon);
            app.subscribeEvent(holon, "MyTopic");
            Console.WriteLine ("Sleeping");
            Thread.Sleep(10);
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

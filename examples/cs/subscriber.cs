 
using System;
using icehms;
using System.Threading;


class Subscriber : Holon
{
    public Subscriber(IceApp app, string name) : base(app, name)
    {
        log("Starting Holon");
        app.subscribeEvent(this, "MyTopic");
    }

    public override void putMessage(hms.Message msg, Ice.Current current)
    {
        log("Got a message from publisher: " + msg);

    }
}


class Test {
    static void Main() {
        Console.WriteLine ("Starting");

        IceApp app = null;
        Subscriber sub = null;
        try
        {
            app = new IceApp("MyTestAdapter", "localhost", 12000);
            sub = new Subscriber(app, "MyTestHolon");
            Thread.Sleep(100000);
            
        }
        catch
        {
            Console.WriteLine("Catcing");
        }
        finally
        {
            if (sub != null )
            {
                sub.shutdown();
            }
            if ( app != null ) 
            {
                app.shutdown();
            }
        }
    }
}

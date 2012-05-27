 
using System;
using icehms;
 
class Test {
    static void Main() {
        Console.WriteLine ("Starting");
        IceApp app = new IceApp("localhost", 12000);
        Console.WriteLine ("Cleanup");
        app.cleanup();
    }
}

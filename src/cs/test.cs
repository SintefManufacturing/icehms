 
using System;
using icehms;
 
class Test {
    static void Main() {
        Console.WriteLine ("Starting");
        IceApp app = new IceApp();
        Console.WriteLine ("Cleanup");
        app.cleanup();
    }
}

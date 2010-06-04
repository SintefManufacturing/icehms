#ifndef _HMS_ICE
#define _HMS_ICE


module hms {
    // special types to be send though ice
    sequence<string> StringSeq; 
    sequence<float> FloatSeq; 
    sequence<double> DoubleSeq; 
    sequence<int> IntSeq; 
    sequence<byte> ByteSeq; // defaults to a python string while other sequences defaults to list !!
    //["python:seq:tuple"] sequence<int> IntTuple; // if we want ice to return tuple and list
    dictionary<string, string> StrStrMap;
	
    // to support messages
    struct Message {
        string address;
        string header;
        string body;
        string creationTime;
        string processingTime;
        StringSeq parameters;
    };

     //Inherited by holons. Agent are used when implemented objects that should not be visible to the HMS
    interface Agent {
        void start();
        void stop();
        string getName();
        bool isRunning();
        StringSeq getPublishedTopics();
        ["ami"] void putMessage(Message s);
        void printMsgQueue();
    };
    
    // base holon to be inherited by all other holons
    interface Holon extends Agent {
        StringSeq getState();   
        void startLogging();
    };
    
    // The PROSA Holons
    interface ResourceHolon extends Holon {
    };

    interface ProductHolon extends Holon {
    };

    interface OrderHolon extends Holon {
    };

    interface StaffHolon extends Holon {
    };

    interface SupervisorHolon extends Holon {
    };

    
    
   interface DeviceAdapter extends Holon { 
       string getDeviceName();
       StrStrMap getDescriptor();
   };

   //Proposition Access control
   interface SimpleAccessControl { 
       double getAccessTimeout();
       bool setAccessTimeout(); // should this be allowed ?
       bool getExclusiveAccess();
       bool releaseExclusiveAccess();
    };
   interface DeviceAdapterAccessCtrled extends DeviceAdapter,SimpleAccessControl { 
   };
    
    
    sequence<double> Vector;
    sequence<Vector> Matrix;
    sequence<Vector> VectorSeq;
    
   
};


#endif 


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

    
    
    // Topics
    // topics must use of those or make declare own
    interface LogMonitor {
        void appendLog(string info);
    };
    
    struct Pos2D {
        double x;
        double y;
    };
    
    interface TopicClient { //attempt to implement a generic topic interface for all holons
        void appendLog(string info);
        void newLog(string info);
        void newState(StringSeq state);
    };
   // The implementation specific holons should be in their own files
    // please remove them

    // Device adapters
    /*
    olivier.roulet@jabber.no: men jeg synes at ideen med en 'DeviceAdapterMedLocking interface som arver DeviceAdapter' er ikke så dum
    Morten på Jabber: nei, det kan hende det er veldig hensiktsmessig
    Morten på Jabber: da må bare strategien for å gi tilgang implementeres i den specifikke klasse
    Morten på Jabber: og jeg tror ikke vi skal kalde det "Lock"
    Morten på Jabber: bedre med "acccess"
    Morten på Jabber: kanskje returverdien er en tid man har access
    Morten på Jabber: kanskje man til metoden kan gi forskjellig spesifikasjon av hvor lenge man vill ha access
    Morten på Jabber: kanskje det må være en getExclusiveAccess, som sikrer at den klienten som får den, er eneste som i den gitte periode kan tilgå
    Morten på Jabber: osv. osv. osv.....
    current.id.name er navnet på holonen 
    current.con.toString() gir ip addressen og port til client og server
    */
   interface DeviceAdapter extends Holon { 
       string getDeviceName();
       StrStrMap getDescriptor();
       //double getExclusiveAccess();
       //bool releaseExclusiveAccess();
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


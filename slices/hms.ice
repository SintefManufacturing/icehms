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

    sequence<double> Vector;
    sequence<Vector> Matrix;
    sequence<Vector> VectorSeq;



	
    // to support messages
    struct Message {
        string address;
        string header;
        string body;
        string sender;
        double createTime;
        StrStrMap arguments;
        //The following members are legacy:
        string creationTime;
        string processingTime;
        StringSeq parameters;
    };

     //To be inherited by holon objects
    interface Holon {
        string getName();
        ["ami"] void putMessage(Message s);
    };
    
    // For people who prefer using Agents
    interface Agent extends Holon {
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
    
    
    
    interface GenericEventInterface {
        ["ami"] void newEvent(string name, StrStrMap arguments, ByteSeq data );
        ["ami"] void putMessage(Message s);
    };

    // A few testing interfaces

    interface SleepHolon { //testing and demo
        bool sleep(double time);
    };

	enum RobotCoordinateSystem { World, Base, Effector, Tool };

	interface RobotMotionCommand extends Holon {
		["ami"] void movel(DoubleSeq pose, double speed, double acc, RobotCoordinateSystem cref);
		DoubleSeq getl(RobotCoordinateSystem cref);
		["ami"] void movej(DoubleSeq pose, double speed, double acc);
		DoubleSeq getj();
	}  ;
   
};


#endif 


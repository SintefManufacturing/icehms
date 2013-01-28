#ifndef _HMS_ICE
#define _HMS_ICE


module hms {
    // commodity types 
    sequence<string> StringSeq; 
    sequence<float> FloatSeq; 
    sequence<double> DoubleSeq; 
    sequence<int> IntSeq; 
    sequence<byte> ByteSeq; 
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
        //legacy members:
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

	enum CSYS { World, Base, Effector, Tool }; //Very robot oriented

	interface GenericRobot extends Holon {
        void setCSYS(CSYS cref);
		["ami"] void movel(DoubleSeq pose, double acc, double vel);
		DoubleSeq getl();
		["ami"] void movej(DoubleSeq pose, double acc, double vel);
		DoubleSeq getj();
		bool isProgramRunning();
        void setDigitalOut(int nb, bool val);
        void setAnalogOut(int nb, bool val);
        bool getDigitalInput(int nb);
        bool getAnalogInput(int nb);
        void setTool(int tool);
        void setTCP(DoubleSeq tcp); 
        void grasp(); // commodity method 
        void release(); // commodity method 
	};
   
};


#endif 


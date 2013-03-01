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
    };


    interface MessageInterface {
        ["ami"] void put_message(Message s);
    };

     //To be inherited by holon objects
    interface Holon extends MessageInterface{
        string get_name();
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

    // a few testing interfaces 

    enum CSYS { World, Base, Effector, Tool }; //Very robot oriented

    interface GenericRobot extends Holon {
        void set_csys(CSYS cref);
        ["ami"] void movel(DoubleSeq pose, double acc, double vel);
        ["ami"] void translate(DoubleSeq pose, double acc, double vel);
        ["ami"] void orient(DoubleSeq pose, double acc, double vel);
        DoubleSeq getl();
        ["ami"] void movej(DoubleSeq pose, double acc, double vel);
        DoubleSeq getj();
        bool is_program_running();
        void set_digital_out(int nb, bool val);
        void set_analog_out(int nb, bool val);
        bool get_digital_input(int nb);
        bool get_analog_input(int nb);
        void set_tool(int tool);
        void set_tcp(DoubleSeq tcp); 
        void grasp(); // commodity method 
        void release(); // commodity method 
    };
   
};


#endif 


#ifndef _MYPROJECT_ICE
#define _MYPROJECT_ICE

#include <hms.ice>

module hms {
    module myproject {
        interface CustomHolon extends Holon {
            double customMethod();
        };
    };
};

module mymodule {
    interface KHolon extends hms::Holon {
         double customMethod();
    };
};



#endif 


from time import  time
import sys

from icehms import LightHolon, BaseHolon, Holon, startHolonStandalone

import hms.myproject
import mymodule

#class TT(hms.myproject.CustomHolon, BaseHolon):
class TT(mymodule.KHolon, LightHolon):
    def __init__(self, name):
        LightHolon.__init__(self, name)

    def customMethod(self, current):
        print "method called"
        return time() 

    def run(self):
        print "I am running !!!!"



if __name__ == "__main__":
    holon = TT("CustomHolon")
    holon.setLogLevel(10)
    startHolonStandalone(holon, logLevel=10)
 



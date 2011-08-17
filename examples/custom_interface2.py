from time import  time
import sys

from icehms import LightHolon, BaseHolon, Holon, startHolonStandalone

import hms.myproject

class TT(hms.myproject.CustomHolon, BaseHolon):
    def __init__(self):
        BaseHolon.__init__(self)

    def customMethod(self, current):
        return time() 

    def run(self):
        print "I am running !!!!"



if __name__ == "__main__":
    holon = TT()
    holon.setLogLevel(10)
    startHolonStandalone(holon, logLevel=10)
 



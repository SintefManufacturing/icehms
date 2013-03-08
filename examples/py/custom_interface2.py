from time import  time
import sys
import logging

from icehms import LightHolon, BaseHolon, Holon, run_holons

import hms.myproject
import mymodule

#class TT(hms.myproject.CustomHolon, BaseHolon):
class TT(LightHolon, mymodule.KHolon):
    def __init__(self, name, logLevel=logging.INFO):
        LightHolon.__init__(self, name, logLevel=logLevel)

    def customMethod(self, current):
        self.logger.info("Custom method of KHolon called")
        return time() 

    def run(self):
        print("I am running !!!!")

class TT2(LightHolon, hms.myproject.CustomHolon):
    def __init__(self, name, logLevel=logging.INFO):
        LightHolon.__init__(self, name, logLevel=logLevel)

    def customMethod(self, current):
        self.logger.info("Custom method of CustomHolon called")
        return time() 

    def run(self):
        self.logger.debug("I am running !!!!")




if __name__ == "__main__":
    holon = TT("KHolon_test1")
    holon2 = TT2("CustomHolon_test2")
    run_holons([holon, holon2])
 



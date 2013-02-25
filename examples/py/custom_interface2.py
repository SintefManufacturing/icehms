from time import  time
import sys
import logging

from icehms import LightHolon, BaseHolon, Holon, run_holon

import hms.myproject
import mymodule

#class TT(hms.myproject.CustomHolon, BaseHolon):
class TT(LightHolon, mymodule.KHolon):
    def __init__(self, name, logLevel):
        LightHolon.__init__(self, name, logLevel=logLevel)

    def customMethod(self, current):
        self.logger.info("Custom method called")
        return time() 

    def run(self):
        print("I am running !!!!")



if __name__ == "__main__":
    holon = TT("CustomHolon")
    run_holon(holon)
 



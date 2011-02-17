from time import  time
import sys

from icehms import Holon, startHolonStandalone

import hms.myproject

class TT(hms.myproject.CustomHolon, Holon):
    def __init__(self):
        Holon.__init__(self)

    def customMethod(self, current):
        return time() 



if __name__ == "__main__":
    holon = TT()
    holon.setLogLevel(10)
    startHolonStandalone(holon, logLevel=10)
 



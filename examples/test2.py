from time import sleep
import sys

from test1 import TestHolon
from icehms import startHolonStandalone



if __name__ == "__main__":
    holon = TestHolon("Holon2")
    holon.setLogLevel(10)
    holon.other = ("Holon1")
    startHolonStandalone(holon, logLevel=10)
 



from time import sleep
import sys

from test1 import TestHolon
from icehms import run_holon



if __name__ == "__main__":
    holon = TestHolon("Holon2")
    holon.other = ("Holon1")
    run_holon(holon)
 



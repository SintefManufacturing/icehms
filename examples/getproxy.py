#!/usr/bin/python
import sys
import atexit
from icehms import IceManager
from time import sleep

def __del__():
    global mgr
    mgr.destroy()

if __name__ == "__main__":
    name = None
    if len(sys.argv) > 1:
        name = sys.argv[1]
    mgr = IceManager()
    mgr.initIce()
    if name:
        prx = mgr.getProxy(name)
        print prx
    #handle bad exit
    atexit.register(__del__)


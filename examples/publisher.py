#!/usr/bin/python

import time
import sys

from icehms import Holon, startHolonStandalone, hms

class Server(Holon):
    def __init__(self):
        Holon.__init__(self, "Server")

    def run(self):
        pub = self._getPublisher("MyTopic", hms.agv.LocalizedPositionPrx)
        counter = 0
        t = time.time()
        while not self._stop:
            p  = hms.agv.Pose()
            p.x = time.time()
            print time.time(), p.x
            p.y = float(counter)
            counter +=1
            p.th = t 
            t = t + 1
            pub.newLocalizedPosition(p)
            time.sleep(0.5)
    
    def getState(self, current):
        return ["Running and publishing"]



if __name__ == "__main__":
    s = Server()
    s.setLogLevel(10)
    startHolonStandalone(s, logLevel=10)

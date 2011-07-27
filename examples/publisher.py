#!/usr/bin/python

import time
import sys
from struct import pack, unpack

from icehms import Holon, startHolonStandalone, hms

class Server(Holon):
    def __init__(self):
        Holon.__init__(self, "Server")

    def run(self):
        #pub = self._getPublisher("MyTopic", hms.GenericEventInterfacePrx)
        pub = self._getEventPublisher("MyTopic")
        counter = 0
        while not self._stop:
            counter +=1
            pub.newEvent("counter", arguments=dict(counter=str(counter)), data=pack("=i", counter) )
            time.sleep(0.5)
    
    def getState(self, current):
        return ["Running and publishing", str(counter)]



if __name__ == "__main__":
    s = Server()
    s.setLogLevel(10)
    startHolonStandalone(s, logLevel=10)

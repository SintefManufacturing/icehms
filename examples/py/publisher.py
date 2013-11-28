#!/usr/bin/python

import time
import sys
from struct import pack, unpack
import logging

from icehms import Holon, run_holon, hms, Message

class Server(Holon):
    def __init__(self, name, logLevel=logging.INFO):
        Holon.__init__(self, name, logLevel=logLevel )

    def run(self):
        #pub = self._get_publisher("MyTopic", hms.GenericEventInterfacePrx)
        pub = self._get_publisher("MyTopic")
        counter = 0
        while not self._stopev:
            counter +=1
            #pub.put_message(Message(header="myHeader", arguments=dict(counter=counter, data=pack("=i", counter) )))
            msg = Message(header="myHeader", body="myBody", arguments=dict(counter=counter, myArgVal="Something", myName=self.name ))
            pub.put_message(msg)
            time.sleep(0.5)
    
    def getState(self, current):
        return ["Running and publishing", str(counter)]



if __name__ == "__main__":
    s = Server("MyPubklisher")
    run_holon(s)

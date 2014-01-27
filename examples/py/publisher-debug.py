#!/usr/bin/python

import time
import sys
from struct import pack, unpack
import logging

from icehms import Holon, run_holons, hms, Message

class Server(Holon):
    def __init__(self, name, logLevel=logging.INFO):
        Holon.__init__(self, name, logLevel=logLevel )

    def run(self):
        pub = self._get_publisher(self.name)
        counter = 0
        while not self._stopev:
            counter += 1
            #pub.put_message(Message(header="myHeader", arguments=dict(counter=counter, data=pack("=i", counter) )))
            msg = Message(header=self.name + "_" + str(counter), body="myBody", arguments=dict(counter=counter, argVal="Something", sender=self.name ))
            pub.put_message(msg)
            time.sleep(0.05)
    


if __name__ == "__main__":
    holons = [Server("MyPublisher" + str(i)) for i in range(100)]
    run_holons(holons)

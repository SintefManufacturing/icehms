#!/usr/bin/python
import sys
from struct import unpack
import logging
from IPython import embed

from icehms import Holon, run_holons, hms

#class Client(Holon, hms.GenericEventInterface):
class Client(Holon):
    def __init__(self, name, tn, logLevel=logging.INFO ):
        Holon.__init__(self, name, logLevel=logLevel )
        self._tn = tn 
        self.counter = 0
        self.received = []

    def run(self):
        #self._subscribeTopic(self._tn)
        self._subscribe_topic(self._tn)

    def put_message(self, msg, current=None):
        #print("Got message: ", msg)
        self.counter += 1
        self.received.append(msg.arguments["counter"])


if __name__ == "__main__":
    holons = [Client("MyTopicClient" + str(i) + "_" + str(j), tn="MyPublisher" + str(j) ) for i in range(20) for j in range(80)]
    run_holons(holons)
    print([h.counter for h in holons])
    #print([h.received for h in holons])
    embed()

#!/usr/bin/python
import sys
from struct import unpack
import logging

from icehms import Holon, run_holons, hms

#class Client(Holon, hms.GenericEventInterface):
class Client(Holon):
    def __init__(self, name, logLevel=logging.INFO ):
        Holon.__init__(self, name, logLevel=logLevel )
        self._tn = "MyTopic"
        self.counter = 0

    def run(self):
        #self._subscribeTopic(self._tn)
        self._subscribe_topic(self._tn)

    def put_message(self, msg, current=None):
        #print("Got message: ", msg)
        self.counter += 1


if __name__ == "__main__":
    holons = []
    for i in range(30):
        holons.append(Client("MyTopicClient" + str(i)))
    run_holons(holons)
    print([h.counter for h in holons])

#!/usr/bin/python
import sys
from struct import unpack
import logging

from icehms import Holon, startHolonStandalone, hms

#class Client(Holon, hms.GenericEventInterface):
class Client(Holon):
    def __init__(self, tn):
        Holon.__init__(self, "MySubscriber", logLevel=logging.INFO )
        self._tn = tn

    def run(self):
        #self._subscribeTopic(self._tn)
        self._subscribeEvent(self._tn)

    def newEvent(self, name, arguments, data, ctx=None):
        if ctx:
            print(ctx.con.toString()) # print my own address and the one from icestorm
        print("New Event: ", name, arguments, "binary data: ", unpack("=i", data)[0])

    def putMessage(self, msg, current=None):
        print("Got message: ", msg)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        topicname = sys.argv[1]
    else:
        topicname = "MyTopic"
    s = Client(topicname)
    startHolonStandalone(s)

#!/usr/bin/python
import sys
from struct import unpack

from icehms import Holon, startHolonStandalone, hms

#class Client(Holon, hms.GenericEventInterface):
class Client(Holon):
    def __init__(self, tn):
        Holon.__init__(self, "Client")
        self._tn = tn

    def run(self):
        self._log("Started")
        self._subscribeTopic(self._tn)

    def newEvent(self, name, stringList, bytesStr, ctx=None):
        print "New Event: ", name, stringList, unpack("=i", bytesStr)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        topicname = sys.argv[1]
    else:
        topicname = "MyTopic"
    s = Client(topicname)
    s.setLogLevel(10)
    startHolonStandalone(s, logLevel=10)

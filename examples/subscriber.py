#!/usr/bin/python
import sys

from icehms import Holon, startHolonStandalone, hms

class Client(Holon, hms.agv.LocalizedPosition):
    def __init__(self, tn):
        Holon.__init__(self, "Client")
        self._tn = tn

    def run(self):
        self.log("Started")
        self._subscribeTopic(self._tn)

    def newLocalizedPosition(self, pose, ctx=None):
        print "New pose: ", pose


if __name__ == "__main__":
    if len(sys.argv) > 1:
        topicname = sys.argv[1]
    else:
        topicname = "MyTopic"
    s = Client(topicname)
    s.setLogLevel(10)
    startHolonStandalone(s, logLevel=10)

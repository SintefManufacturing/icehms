#!/usr/bin/python

import sys

from icehms import IceManager, Holon, startHolonStandalone

class Client(Holon):
    def __init__(self, tn):
        Holon.__init__(self )
        self._tn = tn

    def run(self):
        self._subscribeEvent(self._tn)

    def newEvent(self, name, stringList, bytesStr, ctx=None):
        print "New Event: ", name, stringList, 
        if bytesStr:
            print " and binary data"
        else:
            print ""

    def putMessage(self, msg, ctx=None):
        print "New Message: ", msg 

def print_topics():
    mgr = IceManager()
    mgr.initIce()
    try:
        topics = mgr.eventMgr.retrieveAll()
        print "Events Topics are: \n"
        for name, prx in topics.items():
            print name
    finally:
        mgr.shutdown()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        topicname = sys.argv[1]
    else:
        print "Usage: ", sys.argv[0], " TopicName"
        print ""
        print_topics()
        sys.exit(0)

    s = Client(topicname)
    startHolonStandalone(s)

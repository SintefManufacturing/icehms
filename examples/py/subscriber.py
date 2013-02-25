#!/usr/bin/python
import sys
from struct import unpack
import logging

from icehms import Holon, run_holon, hms

#class Client(Holon, hms.GenericEventInterface):
class Client(Holon):
    def __init__(self, name, logLevel=logging.INFO ):
        Holon.__init__(self, name, logLevel=logLevel )
        self._tn = "MyTopic"

    def run(self):
        #self._subscribeTopic(self._tn)
        self._subscribe(self._tn)

    def put_message(self, msg, current=None):
        print("Got message: ", msg)


if __name__ == "__main__":
    s = Client("MyTopicClient", topicname)
    run_holon(s)

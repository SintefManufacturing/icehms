from time import sleep
import sys
import Ice

from icehms import Holon, startHolonStandalone, Message

class CB(object):
    def ice_response(self, _result=None, l=None):
        print "response: ", _result, l

    def ice_exception(self, ex):
        print "Exception:", ex

class TestHolon(Holon):
    def run(self):
        self.logger.info("I am "+ self.name)
        sleep(0.2) # wait for verything to initialize 
        prx = self._getProxyBlocking(self.other)
        cb = CB()
        while not self._stop:
            masync = Message(body="Async message from "+ self.name, arguments=dict(type="Async Message", name=self.name))
            msync = Message(body="Sync message from "+ self.name)
            try:
                #prx.putMessage_async(cb, masync) # send message async
                self.logger.info("Sending message %s to %s", msync, prx)
                prx.putMessage(msync)
            except Ice.Exception, why:
                self.logger.exception("Exception sending message to %s",  self.other)
            sleep(1)


if __name__ == "__main__":
    import logging
    holon = TestHolon("Holon1", logLevel=logging.INFO)
    holon.other = "Holon2"
    startHolonStandalone(holon)
 


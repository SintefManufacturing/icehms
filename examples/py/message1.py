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
        self._log("I am "+ self.name)
        sleep(0.2) # wait for verything to initialize 
        prx = self._getProxyBlocking(self.other)
        cb = CB()
        while not self._stop:
            masync = Message(body="Async message from "+ self.name, arguments=dict(type="Async Message", name=self.name))
            msync = Message(body="Sync message from "+ self.name)
            try:
                prx.putMessage_async(cb, masync)
                prx.putMessage(msync)
                self._ilog( "State of ",prx.ice_id(), " is ", prx.getState() )
            except Ice.Exception, why:
                self._ilog("Exception running thread:", why)
            sleep(1)


if __name__ == "__main__":

    holon = TestHolon("Holon1")
    holon.setLogLevel(10)
    #holon.enableLogToFile()
    #holon.enableLogToTopic() #Not possible must be call after registreing to ice
    #holon.disableLogToStdout()
    holon.other = ("Holon2")
    startHolonStandalone(holon, logLevel=10)
 

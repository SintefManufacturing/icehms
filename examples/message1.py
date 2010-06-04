from time import sleep
import sys
import Ice

from icehms import Holon, startHolonStandalone, hms
class CB(object):
    def ice_response(self, _result, l):
        print "response: ", _result, l

    def ice_exception(self, ex):
        print "Exception:", ex

class TestHolon(Holon):
    def run(self):
        self._log("I am "+ self.name)
        sleep(0.2) # wait for verything to initialize 
        prx = self._getProxyBlocking(self.other)
        m = hms.Message()
        m.body = "Dummy message from "+ self.name
        cb = CB()
        while not self._stop:
            try:
                prx.putMessage_async(cb, m)
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
 


from time import sleep
import sys
import Ice

from icehms import Holon, startHolonStandalone

class TestHolon(Holon):
    def __init__(self):
        Holon.__init__(self)
    def run(self):
        self._log("I am "+ self.name)
        sleep(0.2) # wait for verything to initialize 
        while not self._stop:
            listprx = self._icemgr.findHolons("::hms::myproject::CustomHolon")
            if listprx:
                for prx in listprx:
                    try:
                        self._ilog( "Calling ",prx.getName(), " customeMethodwhich returns ", prx.customMethod() )
                    except Ice.Exception, why:
                        self._ilog("Exception while querying proxy", why)
            sleep(1)


if __name__ == "__main__":

    holon = TestHolon()
    holon.setLogLevel(10)
    #holon.enableLogToFile()
    #holon.disableLogToStdout()
    startHolonStandalone(holon, logLevel=10)
 


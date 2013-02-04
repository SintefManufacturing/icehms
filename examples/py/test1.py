from time import sleep
import sys
import Ice

from icehms import Holon, startHolonStandalone

class TestHolon(Holon):
    def run(self):
        self._logger.info("I am "+ self.name)
        sleep(0.2) # wait for verything to initialize 
        prx = self._getProxyBlocking(self.other)
        while not self._stop:
            try:
                self._logger.info( "Got info from %s%s ", prx.getName(), prx.ice_id())
            except Ice.Exception, why:
                self._logger.warn("Exception while querying proxy: %s", why)
            sleep(1)

    def getState(self, current):
        #print "CUrrent is ", dir(current),current.id.name, dir(current.con), current.con.toString()
        return ["Running"]


if __name__ == "__main__":
    #import logging
    #logging.basicConfig(level=logging.INFO)

    holon = TestHolon("Holon1")
    #holon.enableLogToFile()
    #holon.enableLogToTopic() #Not possible must be call after registreing to ice
    #holon.disableLogToStdout()
    holon.other = ("Holon2")
    startHolonStandalone(holon)
 


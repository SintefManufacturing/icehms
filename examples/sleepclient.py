
from icehms import Holon, startHolonStandalone
import hms

class SleepClient(Holon):
    def run(self):
        self._log("Starting "+ self.name)
        prx = self._getProxyBlocking("SleepServer")
        print prx.ice_ids()
        prx = prx.ice_timeout(2000)
        for i in (0.1, 0.3, 0.6, 1.0, 2.0, 3.0):
            print "Calling sleep for %f seconds"%i
            prx.sleep(i)
            print "Sleep finished"
        



if __name__ == "__main__":

    holon = SleepClient()
    holon.setLogLevel(10)
    #holon.enableLogToFile()
    #holon.enableLogToTopic() #Not possible must be call after registreing to ice
    #holon.disableLogToStdout()
    startHolonStandalone(holon, logLevel=10)
 


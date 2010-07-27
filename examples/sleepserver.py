from time import sleep

from icehms import Holon, startHolonStandalone
import hms

class SleepHolon(hms.SleepHolon, Holon):
    def __init__(self, name):
        Holon.__init__(self, name)

    def run(self):
        self._log("Starting "+ self.name)
        print self.proxy.ice_ids()

    def sleep(self, s, current):
        sleep(s)
        return True 


if __name__ == "__main__":

    holon = SleepHolon("SleepServer")
    holon.setLogLevel(10)
    #holon.enableLogToFile()
    #holon.enableLogToTopic() #Not possible must be call after registreing to ice
    #holon.disableLogToStdout()
    startHolonStandalone(holon, logLevel=10)
 


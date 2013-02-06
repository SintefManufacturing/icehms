from time import sleep
import sys
import logging

import Ice

from icehms import Holon, startHolonStandalone

class TestHolon(Holon):
    def __init__(self, name):
        Holon.__init__(self, name, logLevel=logging.INFO)
    def run(self):
        self.logger.info("I am "+ self.name)
        while not self._stop:
            listprx = self._icemgr.findHolons("::mymodule::KHolon")
            if listprx:
                for prx in listprx:
                    try:
                        self.logger.info( "Calling %s custom method which returns: %s", prx.getName(), prx.customMethod() )
                    except Ice.Exception as why:
                        self.logger.info("Exception while querying proxy: %s", why)
            else:
                self.logger.info("No KHolon found")
            sleep(1)


if __name__ == "__main__":

    holon = TestHolon("MyServerHolon")
    startHolonStandalone(holon)
 


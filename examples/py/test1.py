from time import sleep
import sys
import Ice

from icehms import Holon, run_holon

class TestHolon(Holon):
    def run(self):
        self.logger.info("I am "+ self.name)
        sleep(0.2) # wait for verything to initialize 
        prx = self._get_proxy_blocking(self.other)
        while not self._stopev:
            try:
                self.logger.info( "The name of proxy is: %s %s ", prx.get_name(), prx.ice_id())
            except Ice.Exception as why:
                self.logger.warn("Exception while querying proxy: %s", why)
            sleep(1)


if __name__ == "__main__":
    import logging
    #logging.basicConfig(level=logging.INFO)
    holon = TestHolon("Holon1", logLevel=logging.INFO)
    holon.other = "Holon2"
    run_holon(holon)
 


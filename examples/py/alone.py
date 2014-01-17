from time import sleep
import sys
import Ice

from icehms import Holon, run_holon

class TestHolon(Holon):
    def run(self):
        self.logger.info("I am "+ self.name)
        sleep(2)  
        self.logger.info("Life is boring, shutting myself down")
        self.shutdown()


if __name__ == "__main__":
    import logging
    #logging.basicConfig(level=logging.INFO)
    holon = TestHolon("HolonAlone", logLevel=logging.INFO)
    run_holon(holon, auto_shutdown=True)
 


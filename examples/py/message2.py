from time import sleep
import sys
from icehms import startHolonStandalone, Holon

class Client(Holon):
    def __init__(self, *args, **kwargs):
        Holon.__init__(self, *args, **kwargs)

    def run(self):
        self.logger.info("Starting waiting for messages")
        while not self._stop:
            if len(self.mailbox) > 0:
                msg = self.mailbox.pop()
                self.logger.info( "got message %s:", msg)
            else:
                sleep(0.1)


if __name__ == "__main__":
    import logging
    holon = Client("Holon2", logLevel=logging.DEBUG)
    startHolonStandalone(holon, logLevel=logging.WARNING)
 



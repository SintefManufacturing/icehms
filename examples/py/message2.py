from time import sleep
import sys
from icehms import run_holon, Holon, hms, Holon_

class Client(Holon):
    def __init__(self, *args, **kwargs):
        Holon.__init__(self, *args, **kwargs)

    def run(self):
        self.logger.info("Starting waiting for messages")
        while not self._stopev:
            if len(self.mailbox) > 0:
                msg = self.mailbox.pop()
                self.logger.info( "got message %s:", msg.body)
            else:
                sleep(0.1)
    #def put_message(self, m, c):
        #print "PPPP"


if __name__ == "__main__":
    import logging
    holon = Client("Holon2", logLevel=logging.DEBUG)
    run_holon(holon, logLevel=logging.WARNING)
 



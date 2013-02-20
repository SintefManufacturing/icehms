from time import sleep

from icehms import Holon, run_holon
import hms

class SleepHolon(hms.SleepHolon, Holon):
    def __init__(self, name):
        Holon.__init__(self, name)

    def run(self):
        print("Starting "+ self.name)
        print(self.proxy.ice_ids())

    def sleep(self, s, current):
        sleep(s)
        return True 


if __name__ == "__main__":

    holon = SleepHolon("SleepServer")
    run_holon(holon)
 


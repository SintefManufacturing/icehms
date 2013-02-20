
from icehms import Holon, run_holon
import hms

class SleepClient(Holon):
    def run(self):
        print("Starting")
        prx = self._get_proxy_blocking("SleepServer")
        print(prx.ice_ids())
        prx = prx.ice_timeout(2000)
        for i in (0.1, 0.3, 0.6, 1.0, 2.0, 3.0):
            print("Calling sleep for %f seconds"%i)
            prx.sleep(i)
            print("Sleep finished")
        



if __name__ == "__main__":

    holon = SleepClient()
    run_holon(holon)
 


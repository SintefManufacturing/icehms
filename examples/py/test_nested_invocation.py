from time import sleep
import sys
from icehms import AgentManager, Holon

class TestHolon(Holon):
    def __init__(self, *args):
        Holon.__init__(self, *args)
        self.other = None 
        self._prx = None

    def run(self):
        while True:
            print 1
            if self.other:
                print 2
                self._prx = self._get_proxy_blocking(self.other)
                break
            if self._stopev:
                return
            sleep(0.2)
        while not self._stopev:
            sleep(1)
            self._log(self.other)

    def hangme(self, ctx=None):
        if self._prx:
            rt = self._prx.getState()
            self._log(rt)
        else:
            self._log("No prx in 1")
        return "MyName" 

    def getState(self, xta=None):
        if self._prx:
            st = self._prx.get_name()
            self._log(st)
            return [st]
        else:
            self._log("No prx in 2")
            return [""]



if __name__ == "__main__":
    holon2 = TestHolon("Holon2")
    holon2.setLogLevel(10)
    holon2.other = ("Holon1")
    holon1 = TestHolon("Holon1")
    holon1.setLogLevel(10)
    holon1.other = ("Holon2")
    mgr = AgentManager()
    mgr.addHolon(holon1)
    mgr.addHolon(holon2)
    sleep(1)

    holon1.hangme()
    sleep(1)
    print "hangme returned"
    mgr.shutdown()
    mgr.waitForShutdown()
 



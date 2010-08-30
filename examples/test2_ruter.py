from time import sleep
import sys

from test1 import TestHolon
from icehms import startHolonStandalone, AgentManager, IceManager



if __name__ == "__main__":
    holon = TestHolon("Holon2")
    holon.setLogLevel(10)
    holon.other = ("Holon1")
    icemgr = IceManager(adapterId="Holon2_adapter", publishedEndpoints="tcp -h eko.sintef.no -p 14000", endpoints="tcp -h 192.168.0.100 -p 10000")
    mgr = AgentManager(icemgr=icemgr, logLevel=10)
    mgr.addHolon(holon)
    mgr.waitForShutdown()
 



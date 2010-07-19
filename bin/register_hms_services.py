#!/usr/bin/env python
import os
import sys
import icehms

action = " add "
if len(sys.argv) > 1:
    action = " update "

cmd = 'icegridadmin --Ice.Default.Locator=IceGrid/Locator:"' +  icehms.IceRegistryServer + '" -e "application ' + action + icehms.iceboxpath + '"'
os.system(cmd)


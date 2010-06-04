#!/usr/bin/env python
import os
import sys
import icehms
import icehms.paths

action = " add "
if len(sys.argv) > 1:
    action = " update "

cmd = 'icegridadmin --Ice.Default.Locator=IceGrid/Locator:"' +  icehms.paths.server + '" -e "application ' + action + icehms.paths.icebox + '"'
os.system(cmd)


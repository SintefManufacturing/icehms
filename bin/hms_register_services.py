#!f:\Python26\python.exe
import os
import subprocess
import sys
import icehms

#Big hack to find ice version
v = str(  icehms.Ice.IcePy.intVersion() )
version = v[0] + v[2]

action = " add "
if len(sys.argv) > 1:
    action = " update "

#cmd = 'icegridadmin --Ice.Default.Locator=IceGrid/Locator:"' +  icehms.IceRegistryServer + '" -e "application ' + action + icehms.iceboxpath + '"'
cmd = 'icegridadmin --Ice.Default.Locator=IceGrid/Locator:"%s" -e "application %s %s ice-version=%s" --username foo --password bar' % (icehms.IceRegistryServer, action, icehms.iceboxpath, version) 
print cmd
p = subprocess.Popen(cmd, shell=True)
rcode = p.wait()


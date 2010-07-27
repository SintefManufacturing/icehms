#!/usr/bin/env  python

import os
import sys

import icehms 

if not os.path.isdir(icehms.nodeData):
    try:
        os.makedirs(icehms.nodeData)
    except os.IOError, why:
        print "Could not create directory for node data, create it and set permission :",icehms.nodeData 
        sys.exit(1)
if not os.path.isdir(icehms.registryData):
    try;
        os.makedirs(icehms.registryData)
    except os.IOError, why:
        print "Could not create directory for registry data, create it and set permission :",icehms.registryData 
        sys.exit(1)


if __name__ == "__main__":
    cmd = "icegridnode"
    cmd += ' --Ice.Config=' + icehms.icecfgpath
    cmd += ' --Ice.Default.Locator="IceGrid/Locator:%s"'%icehms.IceRegistryServer 
    cmd += ' --IceGrid.Registry.Client.Endpoints="%s"'%icehms.IceRegistryServer
    cmd += ' --IceGrid.Registry.Data="%s"'%icehms.registryData
    cmd += ' --IceGrid.Node.Data="%s"'%icehms.nodeData
    if len(sys.argv) > 1: #Add command line arg to iceregistry
        for idx, a in enumerate(sys.argv):
            if idx != 0: #argv[0] is program name
                cmd += " " + a + " "
    print cmd
    os.system(cmd)

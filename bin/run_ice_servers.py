#!/usr/bin/env  python

import os
import sys

import icehms 


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

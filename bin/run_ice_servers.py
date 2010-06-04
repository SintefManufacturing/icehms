#!/usr/bin/env  python

import os
import sys

import icehms 
import icehms.paths


if __name__ == "__main__":
    cmd = "icegridnode"
    cmd += ' --Ice.Config=' + icehms.paths.icecfg 
    cmd += ' --Ice.Default.Locator="IceGrid/Locator:%s"'%icehms.paths.server 
    cmd += ' --IceGrid.Registry.Client.Endpoints="%s"'%icehms.paths.server
    cmd += ' --IceGrid.Registry.Data="%s"'%icehms.paths.registryData
    cmd += ' --IceGrid.Node.Data="%s"'%icehms.paths.nodeData
    if len(sys.argv) > 1: #Add command line arg to iceregistry
        for idx, a in enumerate(sys.argv):
            if idx != 0: #argv[0] is program name
                cmd += " " + a + " "
    print cmd
    os.system(cmd)

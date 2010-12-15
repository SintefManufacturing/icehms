#!/usr/bin/env  python

import os
import sys
import subprocess
import hashlib
from time import sleep

import icehms 

servreg = "hms_register_services.py"
servup = "hms_update_services.py"
if os.name == "nt":
    servreg = os.path.join(sys.prefix, servreg)
    servup = os.path.join(sys.prefix, servup)

if not os.path.isdir(icehms.nodeData):
    try:
        os.makedirs(icehms.nodeData)
    except os.IOError, why:
        print "Could not create directory for node data, create it and set write permissions :", icehms.nodeData 
        sys.exit(1)
if not os.path.isdir(icehms.registryData):
    try:
        os.makedirs(icehms.registryData)
    except os.IOError, why:
        print "Could not create directory for registry data, create it and set write permissions :", icehms.registryData 
        sys.exit(1)


if __name__ == "__main__":
    cmd = "icegridnode"
    cmd += ' --Ice.Config=' + icehms.icecfgpath
    cmd += ' --Ice.Default.Locator="IceGrid/Locator:%s"' % icehms.IceRegistryServer 
    cmd += ' --IceGrid.Registry.Client.Endpoints="%s"' % icehms.IceRegistryServer
    cmd += ' --IceGrid.Registry.Data="%s"' % icehms.registryData
    cmd += ' --IceGrid.Node.Data="%s"' % icehms.nodeData
    if len(sys.argv) > 1: #Add command line arg to iceregistry
        for idx, a in enumerate(sys.argv):
            if idx != 0: #argv[0] is program name
                cmd += " " + a + " "
    print cmd
    icegrid = subprocess.Popen(cmd, shell=True)

    # check if icebox config is up to date
    try:
        f = open(icehms.iceboxpath)
        md5 =  hashlib.md5(f.read())
        md5 = md5.digest()
        hashfile = os.path.join(icehms.db_dir, "hashfile")
        if os.path.isfile(hashfile):
            h = open(hashfile)
            oldmd5 = h.read()
        else:
            oldmd5 = ""
        if md5 != oldmd5 :
            print("Service data have changed , updating db ", md5, oldmd5 )
            sleep(3)
            p = subprocess.Popen(servreg)
            p.wait()
            subprocess.Popen(servup)
            code = p.wait()
            if code == 0:
                h = open(os.path.join(icehms.db_dir, "hashfile"), "w")
                h.write(md5)
        else:
            print "IceBox services are up to date"

        icegrid.wait()
        #os.system(cmd)
    finally:
        icegrid.kill() # I may not kill it here
        if os.name == "nt":
            raw_input("Press Enter to exit...")


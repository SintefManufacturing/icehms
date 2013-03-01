"""
set of hacks to run the IceHMS discovery server
"""

import os
import sys
import subprocess
import hashlib
from time import sleep


import icehms

def update_services():
    return register_services(update=True)

def register_services(update=False):
    #Big hack to find ice version
    v = str(  icehms.Ice.IcePy.intVersion() )
    version = v[0] + v[2]

    if update:
        action = " add "
    else:
        action = " update "

    #cmd = 'icegridadmin --Ice.Default.Locator=IceGrid/Locator:"' +  icehms.IceRegistryServer + '" -e "application ' + action + icehms.iceboxpath + '"'
    cmd = 'icegridadmin --Ice.Default.Locator=IceGrid/Locator:"%s" -e "application %s %s ice-version=%s" --username foo --password bar' % (icehms.IceRegistryServer, action, icehms.iceboxpath, version) 
    print cmd
    p = subprocess.Popen(cmd, shell=True)
    return p.wait()


def make_dirs():
    if not os.path.isdir(icehms.nodeData):
        try:
            os.makedirs(icehms.nodeData)
        except (OSError, IOError):
            print("Could not create directory for node data, create it and set write permissions :", icehms.nodeData) 
            sys.exit(1)
    if not os.path.isdir(icehms.registryData):
        try:
            os.makedirs(icehms.registryData)
        except (OSError, IOError):
            print("Could not create directory for registry data, create it and set write permissions :", icehms.registryData) 
            sys.exit(1)

def check_services(force=False):
    # check if icebox config is up to date
    f = open(icehms.iceboxpath)
    md5 = hashlib.md5(f.read())
    f.close()
    md5 = md5.digest()
    hashfile = os.path.join(icehms.db_dir, "hashfile")
    if os.path.isfile(hashfile):
        h = open(hashfile)
        oldmd5 = h.read()
    else:
        oldmd5 = ""
    if force  or md5 != oldmd5 :
        print("Updating service db in 2 seconds ... ", md5, oldmd5 )
        sleep(2)
        code = register_services()
        code = update_services()
        if code == 0:
            print("update succesfull, writting hash file")
            h = open(os.path.join(icehms.db_dir, "hashfile"), "w")
            h.write(md5)
    else:
        print("IceBox services are up to date")

def clean_registry():
    try:
        imgr = icehms.IceManager()
        imgr.init()
        c = imgr.get_cleaner()
        c.clean()
    finally:
        imgr.shutdown()


def main():
    make_dirs()
    force = False

    cmd = "icegridnode"
    cmd += ' --Ice.Config=' + icehms.icecfgpath
    cmd += ' --Ice.Default.Locator="IceGrid/Locator:%s"' % icehms.IceRegistryServer 
    cmd += ' --IceGrid.Registry.Client.Endpoints="%s"' % icehms.IceRegistryServer
    cmd += ' --IceGrid.Registry.Data="%s"' % icehms.registryData
    cmd += ' --IceGrid.Node.Data="%s"' % icehms.nodeData
    if len(sys.argv) > 1: 
        if sys.argv[1] == "-f":
            force = True
            rest = sys.argv[2:]
        else:
            rest = sys.argv[1:]
        #Add command line args to iceregistry
        for a in rest:
            cmd += " " + a + " "
    print(cmd)

    try:
        icegrid = subprocess.Popen(cmd, shell=True)
        check_services(force)
        sleep(0.5)
        clean_registry()
        icegrid.wait()
        print("Running IceGrid")
        #os.system(cmd)
    finally:
        if os.name == "nt":
            input("Press Enter to exit...")
        try:
            icegrid.kill() 
        except Exception as ex:
            print(ex)
   

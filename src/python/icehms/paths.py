#!/usr/bin/python
"""
Find out where the icehms module is installed
"""
import os
import sys

import icehms 

intree = False
try:
    root = os.environ["ICEHMS_ROOT"]
except KeyError, why:
    root = os.path.realpath(os.path.dirname(__file__))
    root = os.path.normpath(os.path.join(root, "../../../"))
    print "root is ", root
    if os.path.isdir(os.path.join(root, "icecfg")):
        print "Looks like we are in source tree"
        intree = True
    else:
        root = os.path.join(sys.prefix, "share", "icehms")
        if os.path.isdir(root):
            # we are installed
            pass
        else:
            print "Error: set ICEHMS_ROOT environment variable"
            sys.exit(1)

icecfg = os.path.join(root, "icecfg", "icegrid.cfg" ) #configuration
icebox = os.path.join(root, "icecfg", "icebox.xml" ) #configuration
server = icehms.iceconfig.IceRegistryServer #could be deduced, but better use same code as clients
if intree:
    nodeData = os.path.join(root, "db", "node") # node registry
    registryData = os.path.join(root, "db", "registry") #registry database path
else:
    #The code here must be the same as setup.py
    if os.name == "nt":
        db_dir = "c:\icehms_db"
    else:
        db_dir = '/var/lib/icehms/db'
    nodeData = os.path.join(db_dir, "node")
    registryData = os.path.join(db_dir, "registry")


import os
import sys
import re
import exceptions
import Ice


#Find necessary files
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

slicespath = os.path.join(root, "slices") # default slice files
icecfgpath = os.path.join(root, "icecfg", "icegrid.cfg" ) #configuration
iceboxpath = os.path.join(root, "icecfg", "icebox.xml" ) #configuration


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

#Where is the ice registry 
if os.environ.has_key("ICEHMS_REGISTRY"):
    IceRegistryServer = os.environ["ICEHMS_REGISTRY"]
else:
    print "ICEHMS_REGISTRY environment variable not set, using localhost:12000"
    IceRegistryServer = 'tcp -p 12000 ' #we just hope ICe get the right interface



#dynamic compiling Ice slice files
dirs = []

dirs.append(slicespath)

if os.environ.has_key("ICEHMS_SLICES"):
    icehms_slices = os.environ["ICEHMS_SLICES"]
    icehms_slices = icehms_slices.split(";")
    for path in icehms_slices:
        if os.path.isdir(path):
            dirs.append(path)

print "Loading slice files from ", dirs

for path in dirs:
    for icefile in os.listdir(path):
        if re.match("[^#\.].*\.ice$", icefile):
            #print 'icehms.__init__.py: trying to load slice definition:', icefile
            icefilepath = os.path.normpath(os.path.join(path, icefile))
            try:
                Ice.loadSlice("", ["--all", "-I" + path, icefilepath])
            except exceptions.RuntimeError, e:
                print 'icehms.__init__.py: !!! Runtime Error !!!, on loading slice file:', icefile
        else:
            #print 'icehms.__init__.py: not loading non-slice file:', icefile
            pass
        
import hms # only to be able to write "from icehms import hms"

from holon import * # from icehms import holon
from agentmanager import * # from icehms import agentmanager
from icemanager import * # from icehms import icemanager


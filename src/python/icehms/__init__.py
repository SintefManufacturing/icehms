import os
import sys
import re
import exceptions
import Ice

#dynamic compiling Ice slice files
dirs = []
if os.environ.has_key("ICEHMS_ROOT"):
    root = os.environ["ICEHMS_ROOT"]
    dirs.append(os.path.join(root, "slices"))
else:
    #no env variable, maybe we are installed
    slicepath =  os.path.join(sys.prefix, "share", "icehms", "slices")
    if os.path.isdir(slicepath):
        dirs.append(slicepath)
    else:
        path = os.path.realpath(os.path.dirname(__file__))
        path = os.path.normpath(os.path.join(path, "..", "..", "slices"))
        if os.path.isdir(path):
            dirs.append(path)
            print "Seems we are in source tree, loading slices in : ", path
        else:
            print "Did not root icehms slices dir, this is probably an error"

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
import iceconfig # to remove


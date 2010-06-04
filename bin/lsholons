#!/usr/bin/env python

import icehms

mgr = icehms.IceManager()
mgr.initIce()
try:
    objs = mgr.admin.getAllObjectInfos("*")
    print "Holons are :"
    for obj in objs:
        #print obj
        #print dir(obj)
        #print obj.type
        holontype = str(obj.type)
        if holontype.startswith("::hms::"):
            print obj.proxy
finally:
    mgr.shutdown()












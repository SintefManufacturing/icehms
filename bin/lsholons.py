#!/usr/bin/env python

import icehms

mgr = icehms.IceManager()
mgr.initIce()
try:
    objs = mgr.admin.getAllObjectInfos("*")
    print "Holons are :"
    print "Holons are defined as object registered under ::hms:: namespace"
    for obj in objs:
        #print obj
        #print dir(obj)
        #print obj.type
        holontype = str(obj.type)
        if holontype.startswith("::hms::"):
            print obj.proxy
finally:
    mgr.shutdown()












#!/usr/bin/env python

import icehms
import Ice

mgr = icehms.IceManager()
mgr.initIce()
try:
    objs = mgr.admin.getAllObjectInfos("*")
    print "Holons are :"
    print "Holons are defined as object inherinting :hms::Holon"
    for obj in objs:
        #print obj
        #print dir(obj)
        #print obj.type
        holontype = str(obj.type)
        try:
            if obj.proxy.ice_isA("::hms::Holon"):
                print obj.proxy
        except Exception, why:
            print obj.proxy, " seems dead: ", why
finally:
    mgr.shutdown()












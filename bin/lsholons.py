#!/usr/bin/env python

import icehms
import Ice

mgr = icehms.IceManager()
mgr.init()
dead = []
print "Alive holons are :"
try:
    objs = mgr.admin.getAllObjectInfos("*")
    for obj in objs:
        #print obj
        #print dir(obj)
        #print obj.type
        holontype = str(obj.type)
        try:
            if obj.proxy.ice_isA("::hms::Holon"):
                print obj.proxy
        except Exception, why:
            dead.append(obj)
finally:
    mgr.shutdown()

print("\nThe following holons are registered but unreachable:")
for obj in dead:
    print(obj.proxy)












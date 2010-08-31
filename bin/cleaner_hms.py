#!/usr/bin/env python
import sys
import Ice
import IceGrid
import IceStorm

#Ice.loadSlice('hms.ice')
sys.path.append("..")
import re
import icehms
server = icehms.IceRegistryServer 

prop = Ice.createProperties()
prop.setProperty("Ice.Default.Locator","IceGrid/Locator:" + server)
id = Ice.InitializationData()
id.properties = prop
ic = Ice.initialize(id)



registry =  IceGrid.RegistryPrx.uncheckedCast(ic.stringToProxy("IceGrid/Registry"))
session = registry.createAdminSession("olivier", "olivier")
admin  = session.getAdmin()

manager = IceStorm.TopicManagerPrx.checkedCast(ic.stringToProxy("IceStorm/TopicManager"))
#objs = admin.getAllObjectInfos("*")
#for obj in objs:
#    print obj.type
#    print obj.proxy


topics = manager.retrieveAll()

print "Topics: ", topics

for topicName in topics.keys():
    try:
        topic = manager.retrieve(topicName)
    except IceStorm.NoSuchTopic, e:
        print "could not retrive topic from topicmanager"
    else:
        topic.destroy()
        print "topic %s destroyed" % topicName



queryPrx = IceGrid.QueryPrx.checkedCast(ic.stringToProxy("IceGrid/Query"))

objs = admin.getAllObjectInfos("*")
holons = []
for obj in objs:
    #print obj
    #print dir(obj)
    #print obj.type
    holontype = str(obj.type)
    if holontype.startswith("::hms::"):
        holons.append(obj)


print "All Holons: ", holons
for obj in holons:
    try:
        admin.removeObject(obj.proxy.ice_getIdentity())
    except Ice.Exception, why:
        print "Could not de-register holon", obj.proxy, why
    else:
        print "Holon de-registered", obj.proxy



ids = admin.getAllAdapterIds()
print "Adapter: ", ids
if not ids:
    print "No dead adapter found in registry"
for id in ids:
    if re.match(".*\.[Publish,TopicManager].*", id):
        print id, " seems to be part of an IceStorm server...skipping..."
    else:
        print "Removing adapter: ", id
        admin.removeAdapter(id)

#print dir(admin)
ic.shutdown()
ic.waitForShutdown()
ic.destroy()
#topic.unsubscribe(subscriber)










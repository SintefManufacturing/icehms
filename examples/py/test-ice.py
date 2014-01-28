from IPython import embed
import Ice, IceGrid, IceStorm
import sys

properties = Ice.createProperties(sys.argv)
properties.setProperty("hms.AdapterId", "Test_Ice")
myIP = "localhost"
properties.setProperty("hms.Endpoints", "tcp -h {}: udp -h {}".format( myIP, myIP))
properties.setProperty("Ice.Default.Locator", "IceGrid/Locator:" + "tcp -h localhost -p 12000")
properties.setProperty("Ice.Trace.Network", "1")
properties.setProperty("Ice.IPv6", "0")#disable ipv6 as it may hang on some systems
iceid = Ice.InitializationData()
iceid.properties = properties
ic = Ice.initialize(sys.argv, iceid)
try:
    adapter = ic.createObjectAdapter("hms")
    adapter.activate() # allow request
    query = IceGrid.QueryPrx.checkedCast(ic.stringToProxy("IceGrid/Query"))
    registry =  IceGrid.RegistryPrx.uncheckedCast(ic.stringToProxy("IceGrid/Registry"))
    topicMgr = IceStorm.TopicManagerPrx.checkedCast(ic.stringToProxy("IceStorm/TopicManager"))
    messageTopicMgr = IceStorm.TopicManagerPrx.checkedCast(ic.stringToProxy("EventServer/TopicManager"))
    realtimeMgr = IceStorm.TopicManagerPrx.checkedCast(ic.stringToProxy("RealTimeServer/TopicManager"))
    embed()
finally:
    ic.destroy()



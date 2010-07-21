#!/usr/bin/env python
import icehms
mgr = icehms.IceManager()
mgr.initIce()
try:
 
    topics = mgr.topicMgr.retrieveAll()
    print "\nTopics are: \n"
    
    for name, prx in topics.items():
        print name
finally:
    mgr.shutdown()












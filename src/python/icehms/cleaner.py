
import icehms
import logging

class Cleaner(object):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.mgr = icehms.IceManager()
        self.mgr.init()

    def clean_topics(self):
        self._clean_topics(self.mgr.eventMgr)
        self._clean_topics(self.mgr.topicMgr)
    
    def _clean_topics(self, mgr):
        topics = mgr.retrieveAll()
        for topicName, prx in list(topics.items()):
            try:
                topic.destroy()
                self.logger.warn(("topic %s destroyed" % topicName))
            except Exception as ex:
                self.logger.warn(("Could not destroy topic", topic))

    def clean_holons(self):
        holons = self.mgr.findHolons()
        for obj in holons:
            try:
                self.mgr.getAdmin().removeObject(obj.proxy.ice_getIdentity())
            except Ice.Exception as why:
                self.logger.warn("Could not de-register holon", obj.proxy, why)
            else:
                self.logger.warn("Holon de-registered", obj.proxy)

    def clean_adapters(self):
        ids = self.mgr.getAdmin.getAllAdapterIds()
        self.logger.warn("Found adapters: ", ids)
        if not ids:
            self.logger.warn("No dead adapter found in registry")
        for id in ids:
            if re.match(".*\.[Publish,TopicManager].*", id):
                self.logger.warn(id, "%s seems to be part of an IceStorm server...skipping...")
            else:
                self.logger.warn("Removing adapter: %s", id)
                self.mgr.getAdmin().removeAdapter(id)

    def clean(self):
        self.clean_topics()
        self.clean_holons()
        self.clean_adapters()





    def shutdown(self):
        self.mgr.shutdown()

if __name__ == "__main__":
    try:
        c = Cleaner()
        c.clean_topics()
    finally:
        c.shutdown()



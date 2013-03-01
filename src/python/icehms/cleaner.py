"""
Class to remove object in Ice registry databases which can be safely removed
"""
import logging
import Ice
import re

class Cleaner(object):
    def __init__(self, icemgr, logLevel=logging.INFO):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logLevel)
        self.mgr = icemgr 

    def clean_topics(self):
        self._clean_topics(self.mgr.messageTopicMgr)
        self._clean_topics(self.mgr.topicMgr)
    
    def _clean_topics(self, mgr):
        topics = mgr.retrieveAll()
        for name, prx in list(topics.items()):
            try:
                prx.destroy()
                self.logger.info("topic %s destroyed" % name)
            except Exception:
                self.logger.warn("Could not destroy topic %s", name)

    def clean_holons(self):
        holons = self.mgr.find_holons()
        for prx in holons:
            try:
                self.mgr.get_admin().removeObject(prx.ice_getIdentity())
            except Ice.Exception :
                self.logger.warn("Could not de-register holon %s: %s", prx)
            else:
                self.logger.info("Holon %s de-registered", prx)

    def clean_adapters(self):
        ids = self.mgr.get_admin().getAllAdapterIds()
        self.logger.debug("Found adapters: %s", ids)
        if not ids:
            self.logger.info("No dead adapter found in registry")
        for Id in ids:
            if re.match(".*\.[Publish,TopicManager].*", Id):
                self.logger.debug("%s seems to be part of an IceStorm server...skipping...", Id)
            else:
                self.logger.info("Removing adapter: %s", Id)
                self.mgr.get_admin().removeAdapter(Id)

    def clean(self):
        self.clean_topics()
        self.clean_holons()
        self.clean_adapters()



if __name__ == "__main__":
    import icehms
    try:
        imgr = icehms.IceManager()
        imgr.init()
        c = imgr.get_cleaner()
        c.clean()
    finally:
        imgr.shutdown()



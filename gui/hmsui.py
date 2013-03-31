#!/usr/bin/env python
from threading import Lock
import time
import logging

from PyQt4 import QtCore, QtGui, QtDeclarative

from icehms import Holon, AgentManager, LightHolon



class SubscriberHolon(QtCore.QObject, LightHolon):
    newevent = QtCore.pyqtSignal(str, str)

    def __init__(self, topicname, window):
        QtCore.QObject.__init__(self)
        LightHolon.__init__(self)#, logLevel=logging.DEBUG)
        self.window = window
        self.topicname = str(topicname)

    def start(self):
        self.logger.info("Starting subscriber for " + self.topicname)
        self.newevent.connect(self._newEvent)
        self._subscribe_topic(self.topicname)

    def cleanup(self):
        LightHolon.cleanup(self)

    def _newEvent(self, name, msg):
        self.window.newEvent(name, msg)

    def put_message(self, msg, cur):
        #self.newevent.emit(self.topicname, msg.__str__())
        #formating
        self.newevent.emit(self.topicname, msg.header)


class UIHolon(QtCore.QObject, Holon):
    """
    """
    addtopic = QtCore.pyqtSignal(str)
    removetopic = QtCore.pyqtSignal(str)
    addsubscriber = QtCore.pyqtSignal(str)
    removesubscriber = QtCore.pyqtSignal(str)
    def __init__(self, window, logLevel=logging.WARN):
        QtCore.QObject.__init__(self, window)
        Holon.__init__(self, "HMSUIHolon", logLevel=logLevel)
        self.window = window
        self._subscribers = []
        self._lock = Lock()

    def run(self):
        self.addtopic.connect(self._addTopic) #FIXME why cant I connect to qml method directly????
        self.removetopic.connect(self._removeTopic)
        self.addsubscriber.connect(self._add_subscriber)
        self.removesubscriber.connect(self._remove_subscriber)
        self.window.topicDisplayed.connect(self._topicDisplayed)
        self.window.topicHidden.connect(self._topicHidden)
        topics = []
        while not self._stop:
            time.sleep(0.2)
            newtopics = self._icemgr.get_all_topics().keys()
            stopic = set(topics)
            snew = set(newtopics)
            topics = newtopics
            toadd = snew - stopic
            toremove = stopic - snew
            for name in toadd:
                self.addtopic.emit(name)
            for name in toremove:
                self._unsubscribe_topic(name)

    def _topicDisplayed(self, name):
        self.addsubscriber.emit(name) #it looks like we cannot create qt object in thread so we use signals

    def _topicHidden(self, name):
        self.removesubscriber.emit(name)

    def _add_subscriber(self, name):
        with self._lock:
            sub = SubscriberHolon(name, self.window)
            self._agentMgr.add_holon(sub)
            self._subscribers.append(sub)

    def _remove_subscriber(self, name):
        with self._lock:
            for sub in self._subscribers[:]:
                if sub.topicname == name:
                    sub.shutdown()
                    self._subscribers.remove(sub)
                    return

    def _addTopic(self, name):
        self.window.addTopic(name)

    def _removeTopic(self, name):
        self.window.removeTopic(name)



if __name__ == '__main__':
    app = QtGui.QApplication([])
    view = QtDeclarative.QDeclarativeView()
    view.setSource(QtCore.QUrl('view.qml'))
    ctx = view.rootContext()
    root = view.rootObject()
    #root.addTopic("Conveyor1::State")
    #root.addTopic("Cell2::Pull")
    #root.removeTopic("llll")
    #root.displayTopic("kkk")
    #root.displayTopic("llll")
    #root.hideTopic("llll")
    #root.newEvent("Conveyor1::State", "Entering state: Idle")
    view.show()
    mgr = AgentManager("UIAdapter", logLevel=logging.WARN)
    holon = UIHolon(root, logLevel=logging.WARN)
    mgr.add_holon(holon)
    #sub = SubscriberHolon("MyTopic", root)
    #mgr.add_holon(sub)
    try:
        app.exec_()
    finally:
        mgr.shutdown()


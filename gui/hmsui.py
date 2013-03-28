#!/usr/bin/env python
from threading import Lock
import time
from PyQt4 import QtCore, QtGui, QtDeclarative
from icehms import Holon, AgentManager, LightHolon



class SubscriberHolon(QtCore.QObject, LightHolon):
    newevent = QtCore.pyqtSignal(str, str)

    def __init__(self, topicname, window):
        QtCore.QObject.__init__(self)
        LightHolon.__init__(self)
        self.window = window
        self.topicname = str(topicname)

    def start(self):
        self.logger.warn("Starting subscriber for " + self.topicname)
        self.newevent.connect(self._newEvent)
        self._subscribe_topic(self.topicname)

    def stop(self):
        self._unsubscribe_topic(self.topicname)

    def _newEvent(self, name, msg):
        print("Calling newEvent")
        self.window.newEvent(name, msg)

    def put_message(self, msg, cur):
        self.newevent.emit(self.topicname, msg.__str__())


class UIHolon(QtCore.QObject, Holon):
    """
    """
    addtopic = QtCore.pyqtSignal(str)
    removetopic = QtCore.pyqtSignal(str)
    addsubscriber = QtCore.pyqtSignal(str)
    removesubscriber = QtCore.pyqtSignal(str)
    def __init__(self, window):
        QtCore.QObject.__init__(self, window)
        Holon.__init__(self, "HMSUIHolon")
        self.window = window
        self._subscribers = []

    def run(self):
        self.addtopic.connect(self._addTopic) #FIXME why cant I connect to qml method directly????
        self.removetopic.connect(self._removeTopic)
        self.addsubscriber.connect(self._add_subscriber)
        self.removesubscriber.connect(self._remove_subscriber)
        topics = []
        while not self._stop:
            time.sleep(1)
            newtopics = self._icemgr.get_all_topics().keys()
            stopic = set(topics)
            snew = set(newtopics)
            topics = newtopics
            toadd = snew - stopic
            toremove = stopic - snew
            for name in toadd:
                self.addtopic.emit(name)
                self.addsubscriber.emit(name) #it looks like we cannot create qt object in thread so we use signals
            for name in toremove:
                self._unsubscribe_topic(name)
                self.removesubscriber.emit(name)

    def _add_subscriber(self, name):
        print "adding subi:", type(name)
        sub = SubscriberHolon(name, self.window)
        self._agentMgr.add_holon(sub)
        self._subscribers.append(sub)

    def _remove_subscriber(self, name):
        for sub in self._subscribers[:]:
            if sub.topicname == name:
                sub.shutdown()
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
    mgr = AgentManager("UIAdapter")
    holon = UIHolon(root)
    mgr.add_holon(holon)
    #sub = SubscriberHolon("MyTopic", root)
    #mgr.add_holon(sub)
    try:
        app.exec_()
    finally:
        mgr.shutdown()


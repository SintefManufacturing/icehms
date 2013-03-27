#!/usr/bin/env python
from threading import Lock
import time
from PyQt4 import QtCore, QtGui, QtDeclarative
from icehms import Holon, AgentManager




class UIHolon(QtCore.QObject, Holon):
    """
    """
    addtopic = QtCore.pyqtSignal(str)
    removetopic = QtCore.pyqtSignal(str)
    newevent = QtCore.pyqtSignal(str, str)
    def __init__(self, window):
        QtCore.QObject.__init__(self, window)
        Holon.__init__(self, "HMSUIHolon")
        self.window = window
        self._topics = []
        self._holons = []
        self._lock = Lock()
        self._sigs = []

    def run(self):
        #self.connect_sig("Conveyor", "MySignal", self.window.signal1Slot)
        #self.addtopic.connect(self.window.addTopic)
        self.addtopic.connect(self._addTopic) #FIXME why cant I connect to qml method directly????
        self.removetopic.connect(self._removeTopic)
        self.newevent.connect(self._newEvent)
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
            for name in toremove:
                self.removetopic.emit(name)

    def _addTopic(self, name):
        self.window.addTopic(name)
    def _removeTopic(self, name):
        self.window.removeTopic(name)
    def _newEvent(self, name, smg):
        self.window.newEvent(name, msg)



    def put_message(self, msg, cur):
        """
        Override Holon put_message method, this mean nothin arrive in the mailbox
        """
        self.newevent.emit(msg.sender, msg.__str__())



if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)

    view = QtDeclarative.QDeclarativeView()
    #ctx.setContextProperty('myModel', topics)
    view.setSource(QtCore.QUrl('view.qml'))
    ctx = view.rootContext()
    root = view.rootObject()
    root.addTopic("Conveyor1::State")
    root.addTopic("Cell2::Pull")
    #root.removeTopic("llll")
    #root.displayTopic("kkk")
    #root.displayTopic("llll")
    #root.hideTopic("llll")
    root.newEvent("Conveyor1::State", "Entering state: Idle")
    view.show()
    mgr = AgentManager("UIAdapter")
    holon = UIHolon(root)
    mgr.add_holon(holon)
    try:
        app.exec_()
    finally:
        mgr.shutdown()


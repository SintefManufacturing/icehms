#!/usr/bin/env python
from threading import Lock
import time
from PyQt4 import QtCore, QtGui, QtDeclarative
from icehms import Holon, AgentManager




class UIHolon(QtCore.QObject, Holon):
    """
    """
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
        while not self._stop:
            topics = self._icemgr.get_all_topics()

            time.sleep(0.5)


    def connect_sig(self, sender, name, slot):
        """Using old pyqt signal syntax in order to create signals on the fly"""
        sigid = sender + "::" + name 
        signame = sigid + "(PyQt_PyObject, PyQt_PyObject, PyQt_PyObject)"
        print(signame, SIGNAL(signame), slot)
        self.connect(self, SIGNAL(signame), slot)
        with self._lock:
            self._sigs.append((sigid, signame))
        self._subscribe_topic(sigid)

    def _get_msg_vals(self, msg):
        mtype = None
        mname = None
        mval = None
        if msg.arguments.has_key("SignalType"):
            mtype = msg.arguments["SignalType"]
        if msg.arguments.has_key("SignalName"):
            mname = msg.arguments["SignalName"]
        if msg.arguments.has_key("SignalValue"):
            mval = msg.arguments["SignalValue"]
        return (mtype, mname, mval)

    def put_message(self, msg, cur):
        """
        Override Holon put_message method, this mean nothin arrive in the mailbox
        """
        with self._lock:
            stype, sname, sval  = self._get_msg_vals(msg)
            msgid = msg.sender + "::" + sname
            if stype == "BooleanSignal":
                sval = bool(sval)
            elif stype == "IntegerSignal":
                sval = int(sval)
            elif stype == "RealSignal":
                sval = float(sval)
            for sigid, signame in self._sigs:
                if  msgid == sigid:
                    self.emit(SIGNAL(signame), stype, sname, sval)

class DataObject(QtCore.QObject):
    nameChanged = QtCore.pyqtSignal()

    def __init__(self, name, prx):
        super(DataObject, self).__init__()
        self._name = name
        self.prx = prx

    @QtCore.pyqtProperty(str, notify=nameChanged)
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if self._name != name:
            self._name = name
            self.nameChanged.emit()


            
class MyListModel(QtCore.QAbstractListModel): 
    def __init__(self, datain, parent=None, *args): 
        """ datain: a list where each item is a row
        """
        QtCore.QAbstractListModel.__init__(self, parent, *args) 
        self.listdata = datain
 
    def rowCount(self, parent=QtCore.QModelIndex()): 
        return len(self.listdata) 
 
    def data(self, index, role): 
        if index.isValid() and role == Qt.DisplayRole:
            return QtCore.QVariant(self.listdata[index.row()])
        else: 
            return QtCore.QVariant()




if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)

    view = QtDeclarative.QDeclarativeView()
    #ctx.setContextProperty('myModel', topics)
    view.setSource(QtCore.QUrl('view.qml'))
    ctx = view.rootContext()
    root = view.rootObject()
    root.addTopic("kkk")
    root.addTopic("llll")
    #root.removeTopic("llll")
    #root.displayTopic("kkk")
    #root.displayTopic("llll")
    #root.hideTopic("llll")
    root.newEvent("kkk", "New event for kkk")
    view.show()
    mgr = AgentManager("UIAdapter")
    holon = UIHolon(view)
    mgr.add_holon(holon)
    try:
        app.exec_()
    finally:
        mgr.shutdown()


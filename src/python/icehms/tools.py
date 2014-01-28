"""
command line toold of IceHMS
"""

import os
import sys
import subprocess
from time import sleep

import icehms

def update_services():
    return register_services(update=True)

def register_services(update=False):
    #Big hack to find ice version
    v = str(  icehms.Ice.IcePy.intVersion() )
    version = v[0] + v[2]

    if update:
        action = " update "
    else:
        action = " add "

    #cmd = 'icegridadmin --Ice.Default.Locator=IceGrid/Locator:"' +  icehms.IceRegistryServer + '" -e "application ' + action + icehms.iceboxpath + '"'
    cmd = 'icegridadmin --Ice.Default.Locator=IceGrid/Locator:"{}" -e "application {} {} ice-version={} endpoint={}" --username foo --password bar'.format(icehms.IceRegistryServer, action, icehms.iceboxpath, version, "'tcp -h {}'".format(icehms.IceServerHost)) 

    print(cmd)
    p = subprocess.Popen(cmd, shell=True)
    return p.wait()


def make_dirs():
    if not os.path.isdir(icehms.nodeData):
        try:
            os.makedirs(icehms.nodeData)
        except (OSError, IOError):
            print("Could not create directory for node data, create it and set write permissions :", icehms.nodeData)
            sys.exit(1)
    if not os.path.isdir(icehms.registryData):
        try:
            os.makedirs(icehms.registryData)
        except (OSError, IOError):
            print("Could not create directory for registry data, create it and set write permissions :", icehms.registryData)
            sys.exit(1)

def update_icebox_config():
    code = register_services()
    code = update_services()
    if code == 0:
        print("update icebox config succesfull")

def clean_registry():
    try:
        imgr = icehms.IceManager()
        imgr.init()
        c = imgr.get_cleaner()
        c.clean()
    finally:
        imgr.shutdown()


def run_servers():
    make_dirs()

    cmd = "icegridnode"
    cmd += ' --Ice.Config=' + icehms.icecfgpath
    cmd += ' --Ice.Default.Host="{}"'.format(icehms.IceServerHost)
    cmd += ' --Ice.Default.Locator="IceGrid/Locator:%s"' % icehms.IceRegistryServer 
    cmd += ' --IceGrid.Registry.Client.Endpoints="%s"' % icehms.IceRegistryServer
    cmd += ' --IceGrid.Node.Endpoints="tcp -h %s"' % icehms.IceServerHost
    cmd += ' --IceGrid.Registry.Data="%s"' % icehms.registryData
    cmd += ' --IceGrid.Node.Data="%s"' % icehms.nodeData
    if len(sys.argv) > 1: 
        for a in sys.argv[1:]:
            cmd += " " + a + " "
    print(cmd)

    try:
        icegrid = subprocess.Popen(cmd, shell=True)
        sleep(0.5)
        update_icebox_config()
        sleep(0.5)
        clean_registry()
        print("IceHMS servers started")
        icegrid.wait()
    finally:
        if os.name == "nt":
            input("Press Enter to exit...")
        try:
            icegrid.kill() 
        except Exception as ex:
            print(ex)



def lsholons():
    mgr = icehms.IceManager()
    hs = []
    try:
        mgr.init()
        print("The following holons are registered:")
        holons = mgr.find_holons()
        for holon in holons:
            hs.append(holon.__str__())
    finally:
        mgr.shutdown()
    hs.sort()
    for holon in hs:
        print(holon)

def lstopics():
    mgr = icehms.IceManager()
    tps = []
    try:
        mgr.init()
        topics = mgr.get_all_topics()
        print("\nTopics are: \n")
        for name, prx in topics.items():
            tps.append(name)
    finally:
        mgr.shutdown()
    tps.sort()
    for name in tps:
        print(name)


class Client(icehms.Holon):
    def __init__(self, tn):
        icehms.Holon.__init__(self )
        self._tn =  tn
        print("Monitoring all events")

    def get_topics(self):
        topics = self._icemgr.get_all_topics()
        print("Events Topics are: \n")
        top = []
        for name, prx in list(topics.items()):
            top.append(name)
        return top

    def subscribeToAll(self):
        for name in self.get_topics():
            self._subscribe_topic(name)

    def run(self):
        if self._tn:
            self._subscribe_topic(self._tn)
        else:
            self.subscribeToAll()

    def new_event(self, name, stringList, bytesStr, ctx=None):
        pass

    def put_message(self, msg, ctx=None):
        print("New event from: ", msg.sender, msg)

def hms_topic_usage():
    print("Usage: ", sys.argv[0], " [-h|--help] [-a|--all] [TopicName]")
    print("")
    lstopics()
    sys.exit(0)

def hms_topic_print():
    topicname = None
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg in ("-a", "--all"):
            topicname = None
        elif arg in ("-h", "--help"):
            hms_topic_usage()
        else:
            topicname = arg
    else:
        hms_topic_usage()
    s = Client(topicname)
    icehms.run_holon(s)




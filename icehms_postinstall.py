#!/usr/bin/python

import sys
import os

def hack():
    #if someone knows a better way, it would be nice
    #post install stuff
    if os.name == "nt":
        db_dir = "c:\icehms_db"
    else:
        db_dir = '/var/lib/icehms/db'

    print "\n Making %s readable and writable for everybody, change it if necessary\n"%db_dir
    registry = os.path.join(db_dir, "registry") 
    node = os.path.join(db_dir, "node") 
    if not os.path.isdir(registry):
        os.makedirs(registry)
    if not os.path.isdir(node):
        os.makedirs(node)
    os.chmod(db_dir, 0777)  
    os.chmod(registry, 0777) 
    os.chmod(node, 0777)  

    #inform setup.py that we created files
    if globals().has_key("dircetory_created"):
        #we are called from distutil
        directory_created(node)
        directory_created(registry)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "-install":
            hack()
        else :
            pass
            #Nothing to do
    else:
        hack()
    


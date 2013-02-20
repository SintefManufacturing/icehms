#!/usr/bin/python

import sys
import os

def create_windows_menu():
    desktoppath = get_special_folder_path("CSIDL_DESKTOPDIRECTORY")
    menupath = get_special_folder_path("CSIDL_COMMON_PROGRAMS")
    menupath = os.path.join(menupath, "IceHMS")

    # the other links should always work
    apprun = os.path.join(sys.prefix, "Scripts", "run_ice_servers.py")
    appupdate = os.path.join(sys.prefix, "Scripts", "hms_update_services.py")
    appregister = os.path.join(sys.prefix, "Scripts", "hms_register_services.py")
    create_shortcut(apprun, "Run Ice servers", os.path.join(desktoppath, "run_ice.lnk") )

    if not os.path.isdir(menupath):
        try:
            os.makedirs(menupath)
        except Exception, why:
            print "Could not create menus for all users"
        else:
            create_shortcut(apprun, "Run Ice servers", os.path.join(menupath, "run_ice.lnk") )
            #create_shortcut(appregister, "Register Services", os.path.join(menupath, "register_services.lnk" ) )
            #create_shortcut(appupdate, "Update Services", os.path.join(menupath, "update_services.lnk" ) )



    #inform setup.py that we created files
    if globals().has_key("directory_created"):
        #we are called from distutil
        directory_created(menupath)
        file_created(apprun)
        file_created(appupdate)
        file_created(appregister)
    #some warnings from windows
    print """
    IceHMS needs a working Ice and python installation to run
    Install Ice and set the PYTHONPATH and PATH environment variable if necessary (see the Ice documentation)
    """


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] != "-install":
        pass
    if os.name == "nt":
        create_windows_menu()
    if os.name != "nt":
        #ugly hack for debian, not idea, how to avoid it
        os.system("update-python-modules icehms.public")

   


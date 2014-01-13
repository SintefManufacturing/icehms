#!/usr/bin/python

import sys
import os

def create_windows_menu():
    desktoppath = get_special_folder_path("CSIDL_DESKTOPDIRECTORY")
    menupath = get_special_folder_path("CSIDL_COMMON_PROGRAMS")
    menupath = os.path.join(menupath, "IceHMS")
    print("Menu path is: ", menupath)

    # the other links should always work
    print("Creating link to desktop")
    apprun = os.path.join(sys.prefix, "Scripts", "hms_run_servers.exe")
    create_shortcut(apprun, "Run IceHMS servers", os.path.join(desktoppath, "hms_run_servers.lnk") )

    if not os.path.isdir(menupath):
        try:
            os.makedirs(menupath)
        except Exception as why:
            print("Could not create menus for all users")
        else:
            create_shortcut(apprun, "Run IceHMS servers", os.path.join(menupath, "hms_run_servers.lnk") )
            #create_shortcut(appregister, "Register Services", os.path.join(menupath, "register_services.lnk" ) )
            #create_shortcut(appupdate, "Update Services", os.path.join(menupath, "update_services.lnk" ) )



    #inform setup.py that we created files
    if "directory_created" in globals():
        #we are called from distutil
        directory_created(menupath)
        file_created(apprun)
        file_created(appupdate)
        file_created(appregister)
    #some warnings from windows
    print("""
    IceHMS needs a working Ice and python installation to run
    Install Ice and set the PYTHONPATH and PATH environment variable if necessary (see the Ice documentation)
    """)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] != "-install":
        pass
    try:
        create_windows_menu()
    except Exception as ex:
        print(ex)

   


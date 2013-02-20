from distutils.core import setup
from distutils.command.install_data import install_data


import glob
import os

from icehmsversion import VERSION



setup (name = "icehms", 
        version = VERSION,
        description = "Thin Framework to Develop Holonic or Multi-Agent Systems",
        author = "Olivier R-D",
        url = 'https://launchpad.net/icehms',
        packages = ["icehms"],
        package_dir = {'icehms': 'src/python/icehms'},
        license = "GNU General Public License",
        
        scripts = ["bin/hms_print_events", "bin/hms_cleaner", "bin/lsholons", "bin/lstopics", "bin/hms_register_services", "bin/hms_run_servers", "bin/hms_update_services.py", "bin/hms_postinstall.py", "hms_print_all_events"],

        data_files = [('share/icehms/icecfg', glob.glob('icecfg/*')),
                      ('doc/icehms', ["README.txt", "INSTALL.txt"]),
        ('share/icehms/slices', glob.glob('slices/*')) ]

        )

            #("/var/lib/icehms/", ["db"]) ]
        #("bin", ["bin/cleaner_hms", "lsholons", "lstopics", "register_hms_services.py", "run_ice_servers.py", "update_hms_services"])




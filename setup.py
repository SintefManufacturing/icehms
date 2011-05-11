from distutils.core import setup
from distutils.command.install_data import install_data


import glob
import os

VERSION = "0.8.00"

setup (name = "icehms", 
        version = VERSION,
        description = "Thin Framework to Develop Holonic or Multi-Agent Systems",
        author = "Oivier R-D",
        url = 'http://sourceforge.net/projects/coldhms/',
        packages = ["icehms"],
        package_dir = {'icehms': 'src/python/icehms'},
        license = "GNU General Public License",
        
        scripts = ["bin/hms_events.py", "bin/hms_cleaner.py", "bin/lsholons.py", "bin/lstopics.py", "bin/hms_register_services.py", "bin/run_ice_servers.py", "bin/hms_update_services.py", "icehms_postinstall.py"],

        data_files = [('share/icehms/icecfg', glob.glob('icecfg/*')),
                      ('doc/icehms', ["README.txt", "INSTALL.txt"]),
        ('share/icehms/slices', glob.glob('slices/*')) ]

        )

            #("/var/lib/icehms/", ["db"]) ]
        #("bin", ["bin/cleaner_hms", "lsholons", "lstopics", "register_hms_services.py", "run_ice_servers.py", "update_hms_services"])




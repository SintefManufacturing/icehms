from distutils.core import setup
from distutils.command.install_data import install_data


import glob
import os

setup (name = "icehms", version = "0.1",
        description = "Thin Framework to Develop Holonic or Multi-Agent Systems",
        author = "Oivier R-D",
        url = '',
        packages = ["icehms"],
        package_dir = {'icehms': 'src/python/icehms'},
        license = "GNU General Public License",
        
        scripts = ["bin/cleaner_hms", "bin/lsholons", "bin/lstopics", "bin/register_hms_services.py", "bin/run_ice_servers.py", "bin/update_hms_services.py", "postinstall.py"],

        data_files = [('share/icehms/icecfg', glob.glob('icecfg/*')),
        ('share/icehms/slices', glob.glob('slices/*')) ]

        )

            #("/var/lib/icehms/", ["db"]) ]
        #("bin", ["bin/cleaner_hms", "lsholons", "lstopics", "register_hms_services.py", "run_ice_servers.py", "update_hms_services"])




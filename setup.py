from setuptools import setup
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
        
        scripts = ["bin/hms_print_events", "bin/hms_cleaner", "bin/lsholons", "bin/lstopics", "bin/hms_run_servers", "windows_postinstall.py", "bin/hms_print_all_events"],

        data_files = [('share/icehms/icecfg', glob.glob('icecfg/*')),
                      ('doc/icehms', ["README.txt", "INSTALL.txt"]),
        ('share/icehms/slices', glob.glob('slices/*')) ],

        entry_points = {'console_scripts': ['hms_run_servers = icehms.runservers:main']}
        )
    




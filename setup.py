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
        
        scripts = ["bin/hms_topic_print", "bin/lsholons", "bin/lstopics", "windows_postinstall.py"],

        data_files = [('share/icehms/icecfg', glob.glob('icecfg/*')),
                      ('doc/icehms', ["README.txt", "INSTALL.txt"]),
        ('share/icehms/slices', glob.glob('slices/*')) ],

        entry_points = {'console_scripts': ['hms_run_servers = icehms.tools:main', 'hms_cleaner = icehms.tools:clean_registry']}
        )
    




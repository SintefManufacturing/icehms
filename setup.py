from setuptools import setup


import glob
import os



setup (name = "icehms", 
        version = "1.0alpha2",
        description = "Thin Framework to Develop Holonic or Multi-Agent Systems",
        author = "Olivier R-D",
        author_email = "Olivier.roulet@gmail.com",
        url = 'git@github.com:oroulet/icehms.git',
        packages = ["icehms"],
        package_dir = {'icehms': 'src/python/icehms'},
        license = "GNU General Public License",
        
        scripts = ["windows_postinstall.py"],

        data_files = [('share/icehms/icecfg', ["icecfg/icebox.xml", "icecfg/icegrid.cfg"]),
            ('share/doc/icehms', ["README.txt", "INSTALL.txt"]),
            ('share/icehms/slices', ['slices/hms.ice' ])
            ],

        entry_points = {'console_scripts': 
            ['hms_run_servers = icehms.tools:run_servers',
            'lsholons = icehms.tools:lsholons',
            'lstopics = icehms.tools:lstopics',
            'hms_topic_print = icehms.tools:hms_topic_print',
            'hms_cleaner = icehms.tools:clean_registry']
            }
        )
    




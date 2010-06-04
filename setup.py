from distutils.core import setup
from distutils.command.install_data import install_data


import glob
import os

class post_install(install_data):
    def run(self):
        install_data.run(self)
        self._hack()

    def _hack(self):
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

setup (name = "icehms", version = "0.1",
        description = "Thin Framework to Develop Holonic or Multi-Agent Systems",
        author = "Oivier R-D",
        url = '',
        packages = ["icehms"],
        package_dir = {'icehms': 'src/python/icehms'},
        license = "GNU General Public License",
        cmdclass = {"install_data":post_install},
        #package_data = {'icehms': 'data/*'},
        
        scripts = ["bin/cleaner_hms", "bin/lsholons", "bin/lstopics", "bin/register_hms_services.py", "bin/run_ice_servers.py", "bin/update_hms_services"],

        data_files = [('share/icehms/icecfg', glob.glob('icecfg/*')),
        ('share/icehms/slices', glob.glob('slices/*')) ]

        )

            #("/var/lib/icehms/", ["db"]) ]
        #("bin", ["bin/cleaner_hms", "lsholons", "lstopics", "register_hms_services.py", "run_ice_servers.py", "update_hms_services"])




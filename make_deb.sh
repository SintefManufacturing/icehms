rm -r debian
#python setup.py --command-packages=stdeb.command debianize --package="icehms" --section="devel" --depends="python-zeroc-ice" --maintainer="Olivier R-D <olivier@dummyaddress.com>" --debian-version=2
#python setup.py --command-packages=stdeb.command debianize  --workaround-548392=False #workaround if we want it to work with python < 2.6
python setup.py --command-packages=stdeb.command debianize  
echo '#!/bin/sh \npython /usr/bin/icehms_postinstall.py' > debian/icehms.postinst
dpkg-buildpackage -rfakeroot -uc -us

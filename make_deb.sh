#!/bin/sh
set -x
#get version from setup.py file
VERSION=`cat setup.py | grep "VERSION =" | sed s/'VERSION = '// | sed s/\"//g   ` 
rm -r deb_dist
python setup.py --command-packages=stdeb.command sdist_dsc
echo '#!/bin/sh \npython /usr/bin/icehms_postinstall.py' > deb_dist/icehms-$VERSION/debian/icehms.postinst
cd deb_dist/icehms-$VERSION/
dpkg-buildpackage -rfakeroot -uc -us
cd .. 
sudo dpkg -i icehms_${VERSION}-1_all.deb

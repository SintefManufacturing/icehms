#!/bin/sh
set -x
VERSION=0.6.7
rm -r deb_dist
python setup.py --command-packages=stdeb.command sdist_dsc
echo '#!/bin/sh \npython /usr/bin/icehms_postinstall.py' > deb_dist/icehms-$VERSION/debian/icehms.postinst
cd deb_dist/icehms-$VERSION/
dpkg-buildpackage -rfakeroot -uc -us

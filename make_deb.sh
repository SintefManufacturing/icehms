#!/bin/bash
#set -x

function check_deb {

    dpkg -s $1 > /dev/null
    if [ `echo $?` != 0 ] ; then
        echo "please install $1"
        exit 1
    fi
}
#we need stdeb
check_deb python-stdeb
check_deb build-essential

#get version from setup.py file
VERSION=`cat setup.py | grep "VERSION =" | sed s/'VERSION = '// | sed s/\"//g   ` 
rm -r deb_dist
python setup.py --command-packages=stdeb.command sdist_dsc
echo -e '#!/bin/sh \npython /usr/bin/icehms_postinstall.py' > deb_dist/icehms-$VERSION/debian/icehms.postinst
cd deb_dist/icehms-$VERSION/
dpkg-buildpackage -rfakeroot -uc -us
cd .. 
echo -e "\n Install package ?(y/n)\n"
read ANS
if [ X"$ANS" = "Xy" ]; then 
    sudo dpkg -i icehms_${VERSION}-1_all.deb
else
    echo "OK, not installing"
fi

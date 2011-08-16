#!/bin/bash
#set -x

function check_deb {

    dpkg -s $1 > /dev/null
    if [ `echo $?` != 0 ] ; then
        echo "please install $1"
        exit 1
    fi
}

check_deb build-essential

#get version from setup.py file
VERSION=`cat setup.py | grep "VERSION =" | sed s/'VERSION = '// | sed s/\"//g   ` 
VERSION="$VERSION-`bzr version-info --check-clean --custom --template='{revno}'`"
#hack debian changelog
cat debian_changelog_template.txt | sed   -e "s/VERSION/$VERSION/g" | sed   -e "s/DATE/`date --rfc-2822`/g" > debian/changelog

#rm -r deb_dist
#python setup.py --command-packages=stdeb.command sdist_dsc
#echo -e '#!/bin/sh \npython /usr/bin/icehms_postinstall.py' > deb_dist/icehms-$VERSION/debian/icehms.postinst
#cd deb_dist/icehms-$VERSION/
dpkg-buildpackage -rfakeroot -uc -us -b
echo -e "\n Install package ?(y/n)\n"
read ANS
if [ X"$ANS" = "Xy" ]; then 
    sudo dpkg -i ../icehms_${VERSION}_all.deb
else
    echo "OK, not installing"
fi

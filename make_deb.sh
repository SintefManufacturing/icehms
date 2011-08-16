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

BZRVERSION="bzr`bzr version-info --check-clean --custom --template='{revno}'`"
#hack debian changelog
cat debian_changelog_template.txt | sed   -e "s/VERSION/08-$BZRVERSION/g" | sed   -e "s/DATE/`date --rfc-2822`/g" > debian/changelog

dpkg-buildpackage -rfakeroot -uc -us -b

DEB=`ls -t1 ../*.deb | head -n1`
echo -e "\n Install package $DEB?(y/n)\n"
read ANS
if [ X"$ANS" = "Xy" ]; then 
    sudo dpkg -i $DEB
else
    echo "OK, not installing"
fi

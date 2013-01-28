import subprocess
from icehmsversion import VERSION
from email.Utils import formatdate

def check_deb(name):
    print("checking if %s is installed" % name)
    subprocess.check_call("dpkg -s %s > /dev/null" % name, shell=True)

if __name__ == "__main__":
    check_deb("build-essential")


    #creating simple changelog for debian
    subprocess.check_call("cat debian_changelog_template.txt | sed   -e 's/VERSION/%s/g' | sed   -e 's/DATE/%s/g' > debian/changelog" % (VERSION, formatdate()), shell=True)

    #now build package
    subprocess.check_call("dpkg-buildpackage -rfakeroot -uc -us -b", shell=True)



    lastdeb = subprocess.check_output("ls -t1 ../*.deb | head -n1", shell=True)

    ans = input("\n\n Install Package %s? (N,y)" % lastdeb)
    if ans in ("y", "Y"):
        print("sudo dpkg -i %s" % lastdeb)
        subprocess.check_call("sudo dpkg -i %s" % lastdeb, shell=True)
    else:
        print("OK, not installing")




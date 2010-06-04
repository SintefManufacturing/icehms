prefix=/usr

all:
	python setup.py build

install: 
	#debian/ubuntu
	python setup.py install --prefix=/usr --force --install-layout=deb
	#others ??
	#python setup.py install --prefix=/usr --force 

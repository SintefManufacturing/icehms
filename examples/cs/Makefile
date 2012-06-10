
MCS=dmcs
SLICEDIR=../../slices/
LIB=icehms.dll

all: publisher.exe subscriber.exe

%.exe: %.cs
	$(MAKE) -C ../../src/cs/
	$(MCS) -debug -define:DEBUG -target:exe -out:$@ -r:$(LIB) -pkg:Ice-3.4,IceGrid-3.4,IceStorm-3.4 $<




clean:
	rm -f publisher.exe
	rm -f subscriber.exe

.PHONY: all clean


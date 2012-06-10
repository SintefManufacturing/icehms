
MCS=dmcs
SLICEDIR=../../slices/

all: icehms.dll

icehms.dll: icehms.cs hms.cs
	$(MCS) -debug -define:DEBUG -target:library -out:$@ -pkg:Ice-3.4,IceGrid-3.4,IceStorm-3.4 $+

hms.cs: $(SLICEDIR)/hms.ice
	slice2cs --tie $<


clean:
	rm -f hms.cs
	rm -f icehms.dll

.PHONY: all clean


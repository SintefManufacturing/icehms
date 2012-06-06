slice2cs --tie ../../slices/hms.ice
dmcs -debug -define:DEBUG -target:library -out:icehms.dll -pkg:Ice-3.4,IceGrid-3.4,IceStorm-3.4 icehms.cs hms.cs

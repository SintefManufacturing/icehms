slice2cs --tie ../../slices/hms.ice
dmcs -debug -define:DEBUG -target:library -out:icehms.dll -pkg:Ice-3.4,IceGrid-3.4,IceStorm-3.4 test.cs icehms.cs hms.cs
dmcs -debug -define:DEBUG -target:exe -out:test.exe -r:icehms.dll  -pkg:Ice-3.4,IceGrid-3.4,IceStorm-3.4 test.cs 
dmcs -debug -define:DEBUG -target:exe -out:test2.exe -r:icehms.dll  -pkg:Ice-3.4,IceGrid-3.4,IceStorm-3.4 test2.cs 

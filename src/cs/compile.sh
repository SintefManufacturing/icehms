slice2cs ../../slices/hms.ice
dmcs -warnaserror -debug -define:DEBUG -target:library -out:icehms.dll -pkg:Ice-3.4,IceGrid-3.4,IceStorm-3.4 test.cs icehms.cs hms.cs
dmcs -warnaserror -debug -define:DEBUG -target:exe -out:test.exe -r:icehms.dll  -pkg:Ice-3.4,IceGrid-3.4,IceStorm-3.4 test.cs 

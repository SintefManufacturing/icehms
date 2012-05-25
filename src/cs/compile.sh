slice2cs ../../slices/hms.ice
gmcs -warnaserror -debug -define:DEBUG -out:test.exe -pkg:Ice-3.4,IceGrid-3.4,IceStorm-3.4 test.cs icehms.cs hms.cs

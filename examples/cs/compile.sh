cp -v ../../src/cs/icehms.dll .
dmcs -debug -define:DEBUG -target:exe -out:test.exe -r:icehms.dll  -pkg:Ice-3.4,IceGrid-3.4,IceStorm-3.4 test.cs -lib:../../src/cs/
dmcs -debug -define:DEBUG -target:exe -out:test2.exe -r:icehms.dll  -pkg:Ice-3.4,IceGrid-3.4,IceStorm-3.4 test2.cs -lib:../../src/cs/
dmcs -debug -define:DEBUG -target:exe -out:publisher.exe -r:icehms.dll  -pkg:Ice-3.4,IceGrid-3.4,IceStorm-3.4 publisher.cs -lib:../../src/cs/
dmcs -debug -define:DEBUG -target:exe -out:subscriber.exe -r:icehms.dll  -pkg:Ice-3.4,IceGrid-3.4,IceStorm-3.4 subscriber.cs -lib:../../src/cs/


import os

#hack to set the same IceGridRegistry server for all clients
if os.environ.has_key("ICEHMS_REGISTRY"):
    IceRegistryServer = os.environ["ICEHMS_REGISTRY"]
else:
    print "ICEHMS_REGISTRY environment variable not set, using localhost:12000"
    IceRegistryServer='tcp -p 12000 ' #we just hope ICe get the right interface

#print "Using %s as registry address"%IceRegistryServer

IceTimeout = 500 #default timeout in ms for all proxy objects. This is more than enough on our network


#!/bin/sh

#if icehms is installed in usuall place this may be necessary
#export ICEHMS_ROOT=$HOME/icehms/

# where the registry server is
#default is locahost 12000
#export ICEHMS_REGISTRY="tcp -p 12000 -h tlpc484.sintef.no"
export ICEHMS_REGISTRY="tcp -p 12000 -h localhost"

#if icehms is not installed we need to tell python where the python files are
#export PYTHONPATH=$ICEHMS_ROOT/python/:$PYTHONPATH

# tell icehms where to load optional ice slices file
#export ICEHMS_SLICES="$HOME/MyProject/MySlices/;$HOME/MyProject2/Slices"
#export ICEHMS_SLICES="$HOME/initcode/slices"

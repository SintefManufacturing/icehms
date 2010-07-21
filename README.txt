

icehms is holonic framework based on "The Internet Communication Engine"(Ice)

It requires an ice and python installation 

This a prototype and many things may not work


#if icehms is installed in an unsuall place,  this may be necessary
#export ICEHMS_ROOT=$HOME/icehms/

# Define where the registry server is, the default is locahost 12000
#export ICEHMS_REGISTRY="tcp -p 12000 -h tlpc484.sintef.no"
export ICEHMS_REGISTRY="tcp -p 12000 -h localhost"

#if using python and icehms is not installed we need to tell python where the python files are
#export PYTHONPATH=$ICEHMS_ROOT/python/:$PYTHONPATH

# tell icehms where to load optional ice slices file
#export ICEHMS_SLICES="$HOME/MyProject/MySlices/;$HOME/MyProject2/Slices"
#export ICEHMS_SLICES="$HOME/initcode/slices"

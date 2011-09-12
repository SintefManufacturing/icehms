
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.


icehms is holonic framework based on "The Internet Communication Engine"(Ice)

It requires an ice and python installation 

This is a prototype and many things may not work


#if icehms is installed in an unsuall place,  this may be necessary
#export ICEHMS_ROOT=$HOME/icehms/

# Define where the registry server is, the default is locahost 12000
#export ICEHMS_REGISTRY="tcp -p 12000 -h tlpc484.sintef.no"
export ICEHMS_REGISTRY="tcp -p 12000 -h localhost"

# you may also need to setup PYTHONPATH 
#export PYTHONPATH=$ICEHMS_ROOT/python/:$PYTHONPATH

# slices files defining the interface of your objects may be installed in different places
# first they can be installed system width
# then you can have them in the local directory
# or you can have user slice files in ~/.icehms/slices/
# or you can tell icehms where to load optional ice slices file
#export ICEHMS_SLICES="$HOME/MyProject/MySlices/;$HOME/MyProject2/Slices"
#export ICEHMS_SLICES="$HOME/initcode/slices"


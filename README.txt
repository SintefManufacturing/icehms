
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


IceHMS is holonic or multi-agent framework based on "The Internet Communication Engine"(Ice). 
It has been implemented to facilitate the development of holonic situated multi-agent systems.
It requires Ice and Python to be installed. This is a prototype and many things may not work

if IceHMS is installed in an unusual place, this may be necessary: 
export ICEHMS_ROOT=$HOME/icehms/

Define where the registry server is, the default is localhost 12000:
export ICEHMS_REGISTRY="tcp -p 12000 -h tlpc484.sintef.no"
export ICEHMS_REGISTRY=p -p 12000 -h localhost"
#alternative you may do this programmatically after importing icehms in python: icehms.IceRegistrServer = "tcp -p 12000 -h localhost"

you may also need to setup PYTHONPATH: 
export PYTHONPATH=$ICEHMS_ROOT/python/:$PYTHONPATH

slices files defining the interface of your objects may be installed in different places:
they can be installed system width
then you can have them in the local directory
or you can have user slice files in ~/.icehms/slices/
or you can tell IceHMS where to load optional ice slices file
export ICEHMS_SLICES="$HOME/MyProject/MySlices/;$HOME/MyProject2/Slices"
export ICEHMS_SLICES="$HOME/initcode/slices"


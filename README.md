# iCOW
island City On a Wedge, a modeling framework of intermediate complexity

Copyright (C) 2019  Robert L. Ceres

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

Code used in this archive was used to develop all figures in Ceres, Forest, Keller, 2019.

The BORG multiple objective evolutionary algorithm is required for this application. BORG is described and available at: https://github.com/Project-Platypus/Platypus. The Python version included in this archive is used by permission,
http://borgmoea.org. Follow the instructions on the Platypus github for installing and setting up the BORG MOEA.

Software included in this archive is written in Python and C. Shell scripts are provided to execute the code within a PBS unix environment (although this is not strictly necessary). A makefile is included. C source code is included in the src subfolder. When compiled correctly the C code produces a dynamic link library that is used by the python scripts to actually conduct the optimization. The makefile is configured for a Unix system and produces the file icow.dylib which must be located in the path.

The main program accesses a surges.bin file containing annual highest storm surges. This file format may be dependant on machine hardware or software configuration. An RData file consisting of the storm surge sequences is contained in the src subfolder along with R and C code if required to generate the storm surge bin file.

Once the software is compiled the shell scripts in the subfolder 81c can be executed. These shell scripts contain the command line parameters used for figures in the paper. They execute the python scripts in the main directory that optimize the iCOW for various combinations of lever settings.

Other Python scripts are provided for generating figures.

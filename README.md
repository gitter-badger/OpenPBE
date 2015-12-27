#OpenPBE

An implementation of population balance solution strategies for OpenFOAM.

## Copyright information

    Copyright (C) 2013-2015
    OpenPBE developers
    Cranfield University, UK

## License
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

## Development objectives

 * Develop the ports for OF3.0 solves
 * Implement method of classes (MOC)
 * Implement quadrature method of moments (QMOM)
 * Develop consistent testing framework

## Build

```bash
# Clone the project

# Load OpenFOAM environment

cd <project_dir>

# Donload benchmark
git submodule init
git submodule update 

# Build the project
mkdir build
cmake ../
make # alternatively make -j 4 for parallell build
```

## Usage

The current version uses canonical `twoPhaseEulerFoam`. The only necessary
change is to include

```
libs ("libPBE.so")
``` 

in your `controlDict`. See `testing/twoPhaseEulerFoam` for the full setup.

#!/bin/bash

yum -y update || exit 1
yum -y install boost boost-devel gmp  gmp-devel  mpfr  mpfr-devel vtk-devel || exit 1

# Install CGAL from source
wget https://github.com/CGAL/cgal/releases/download/v5.6.1/CGAL-5.6.1.tar.xz
tar xf CGAL-5.6.1.tar.xz
cd CGAL-5.6.1 || exit 1
cmake -DCMAKE_BUILD_TYPE=Release .
make install || exit 1
rm -rf cd CGAL-5.6.1

# Install opencascade
wget https://github.com/Open-Cascade-SAS/OCCT/archive/refs/tags/V7_8_1.tar.gz && tar xzf V7_8_1.tar.gz && rm V7_8_1.tar.gz || exit 1
cd OCCT-7_8_1 && cmake . && make install || exit 1
cd .. && rm -rf OCCT-7_8_1 || exit 1

# Install ROOT
root_version="6.32.04"
ROOTSYS="/opt/root"

mkdir -p "$ROOTSYS" || exit 1
wget -q -O- "https://root.cern/download/root_v${root_version}.Linux-fedora39-x86_64-gcc13.3.tar.gz" \
    | tar --strip-components 1 -C "$ROOTSYS" --strip=1 -x -z || exit 1

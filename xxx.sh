#!/bin/bash
cd cpp_libs

# create build directories
mkdir -p build/python/build

# build C++ code
cd build
cmake ..
cmake --build .
cd ..

# build Python module
cd python
mkdir build
cd build
cmake .. -DPYTHON_LIBRARY_DIR="c:\users\omarj\miniconda3\envs\sci\lib\site-packages" -DPYTHON_EXECUTABLE="c:\Users\omarj\miniconda3\envs\sci\python"
cmake --build .
mv Debug/pyimg.cp38-win_amd64.pyd Debug/pyimg.pyd

# install Python module
cp -f Debug/pyimg.pyd c:\users\omarj\miniconda3\envs\sci\lib\site-packages

PYIMG_PATH=$(realpath Debug/pyimg.pyd)
export PYTHONPATH=${PYTHONPATH/$PYIMG_PATH:/} # remove old path
export PYTHONPATH=$(dirname $PYIMG_PATH):$PYTHONPATH # add new path
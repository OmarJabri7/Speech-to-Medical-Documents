# # python setup.py build_ext --inplace
# cd cpp_libs
# mkdir build
# cd build
# cmake ../
# cmake --build .
# cd ..
# cd python
# mkdir build
# cmake ../
# cmake --build .
# # cd ../..
# # cpp_libs/build/bin/Debug/ramosa_med.exe


cd cpp_libs
mkdir build
cd build
cmake ..
cmake --build .
cd ..
cd python
mkdir build
cd build 
cmake .. -DPYTHON_LIBRARY_DIR="c:\users\omarj\miniconda3\envs\sci\lib\site-packages" -DPYTHON_EXECUTABLE="c:\Users\omarj\miniconda3\envs\sci\python"
cmake --build .
mv Debug/pyimg.cp38-win_amd64.pyd Debug/pyimg.pyd
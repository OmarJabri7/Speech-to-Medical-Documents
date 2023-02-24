from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np

ext_modules = [Extension("utils.extractor",
                         sources=["utils/extractor.pyx"],
                         include_dirs=[np.get_include()])]

setup(
    name='my_package',
    ext_modules=cythonize(ext_modules),
    include_dirs=[np.get_include()]
)

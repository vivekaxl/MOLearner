from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("non_dominated_sort_fast.pyx")
)
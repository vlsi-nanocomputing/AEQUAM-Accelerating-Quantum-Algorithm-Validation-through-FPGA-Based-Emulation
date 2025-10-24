#Setup.py
#create in 22/05/2023 by Deborah Volpe
#this file compile the cpp cores for their integration in python code

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from Cython.Build import cythonize

setup(
    name='SoftwareEmulatorFixedPointNearestEven',
    ext_modules=cythonize([Extension(name='VLSIEmulatorFixedNearestEven',
                                     sources=['emulator_wrapper_fixed_ne.pyx', 'emulator_fixed_nearest_even.cpp'],
                                     depends=["emulator_fixed_nearest_even.h"],
                                     include_dirs=['./'],
                                     language='c++')]),
    cmdclass={'build_ext': build_ext},
)

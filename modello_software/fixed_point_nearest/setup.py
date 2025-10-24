#Setup.py
#create in 22/05/2023 by Deborah Volpe
#this file compile the cpp cores for their integration in python code

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from Cython.Build import cythonize

setup(
    name='SoftwareEmulator_fixed_nearest',
    ext_modules=cythonize([Extension(name='VLSIEmulatorFixedPointNearest',
                                     sources=['emulator_wrapper_fixed_nearest.pyx', 'emulator_fixed_nearest.cpp'],
                                     depends=["emulator_fixed_nearest.h"],
                                     include_dirs=['./'],
                                     language='c++')]),
    cmdclass={'build_ext': build_ext},
)

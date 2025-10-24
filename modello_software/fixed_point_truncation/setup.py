#Setup.py
#create in 22/05/2023 by Deborah Volpe
#this file compile the cpp cores for their integration in python code

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from Cython.Build import cythonize

setup(
    name='SoftwareEmulatorFixed',
    ext_modules=cythonize([Extension(name='VLSIEmulatorFixedPoint',
                                     sources=['emulator_wrapper_fixed.pyx', 'emulator_fixed.cpp'],
                                     depends=["emulator_fixed.h"],
                                     include_dirs=['./'],
                                     language='c++')]),
    cmdclass={'build_ext': build_ext},
)

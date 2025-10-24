#Setup.py
#create in 22/05/2023 by Deborah Volpe
#this file compile the cpp cores for their integration in python code

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from Cython.Build import cythonize

setup(
    name='SoftwareEmulator',
    ext_modules=cythonize([Extension(name='VLSIEmulator',
                                     sources=['emulator_wrapper.pyx', 'emulator.cpp'],
                                     depends=["emulator.h"],
                                     include_dirs=['./'],
                                     language='c++')]),
    cmdclass={'build_ext': build_ext},
)

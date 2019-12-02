#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tuesday 12.02.2019
@author: Ahmed Qamesh
"""
from setuptools import setup, find_packages
from __version__ import __version__
from distutils.core import setup
with open("README.md", "r") as fh:
    long_description = fh.read()
__author__ = 'Ahmed Qamesh'

setup(name='XrayIrradiationBonn',
      version=__version__,
      url='ahmed.qamesh@cern.ch',
      description='Xray Irradiation System at Bonn University',
      long_description=long_description,
      long_description_content_type="text/markdown",
      classifiers=['Development Status :: 3 - Alpha',
                   'License :: Freeware',
                   'Intended Audience :: Science/Research',
                   'Programming Language :: Python :: 3.6',
                   'Topic :: Scientific/Engineering :: Physics'],
      author='Ahmed Qamesh',
      author_email='ahmed.qamesh@cern.ch',
      packages=find_packages(),
      install_requires=['coloredlogs', 'verboselogs'],
      include_package_data=True,
      entry_points={'console_scripts':
                    ['XrayIrradiationBonn=CalibrationCurve_Bonn:main']}
      )

#!/usr/bin/env python
# -*- coding: utf-8 -*-

#The MIT License (MIT)
#Copyright (c) 2015 Alexandre LM, Dimitri S

from setuptools import setup, find_packages

#Open requirements
with open('./requirements.txt') as f:
    required = f.read().splitlines()

import pygnata

# Initiate the setup function
setup(

    # The lib name for pypi
    name='pygnata',

    # The pygnata version
    version=pygnata.__version__,

    #Find all the package to insert
    packages=find_packages(),
    author="Alexandre LM, Dimitri S",
    author_email="pygnata@tutanota.com",
    description="Generator of projects tree from template",
    long_description=open('README.md').read(),
    install_requires= required ,
    include_package_data=True,
    url='https://github.com/joviaux/pygnata',

    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: French",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development",
    ],

    entry_points = {
        'console_scripts': [
            'pygnata = pygnata.pygnata:pygnata_run',
        ],
    },
)

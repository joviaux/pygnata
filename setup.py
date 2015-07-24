#!/usr/bin/env python
# -*- coding: utf-8 -*-

#The MIT License (MIT)
#Copyright (c) 2015 Alexandre LM, Dimitri S
import os
from setuptools import setup, find_packages

#Open requirements
with open(os.path.join(os.path.dirname(__file__),'requirements.txt')) as f:
    required = f.read().splitlines()

# Initiate the setup function
setup(

    # The lib name for pypi
    name='pygnata',

    # The pygnata version
    version="0.0.3",

    #Find all the package to insert
    packages=find_packages(),
    author="Alexandre LM, Dimitri S",
    author_email="pygnata@tutanota.com",
    description="Generator of projects tree from template",
    long_description='https://github.com/joviaux/pygnata/blob/master/README.md',
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

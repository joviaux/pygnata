#!/usr/bin/env python
# -*- coding: utf-8 -*-

#The MIT License (MIT)
#Copyright (c) 2015 Alexandre LM, Dimitri S

from setuptools import setup, find_packages
from pip.req import parse_requirements

#Open requirements
install_reqs = parse_requirements('./requirements.txt', session=False)
required = [str(ir.req) for ir in install_reqs]

# Initiate the setup function
setup(

    # The lib name for pypi
    name='pygnata',

    # The pygnata version
    version="0.0.1",

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

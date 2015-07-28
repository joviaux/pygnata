# -*- coding: utf-8 -*-
from path import path

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

#Set the path of the current file
current = path(__file__)
pygconfig = configparser.SafeConfigParser()
#Load the config file
pygconfig.read(current.parent / 'pygnata.conf')

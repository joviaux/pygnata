# -*- coding: utf-8 -*-
import configparser
from path import path

#Set the path of the current file
current = path(__file__)
pygconfig = configparser.SafeConfigParser()
#Load the config file
pygconfig.read(current.parent / 'pygnata.conf')

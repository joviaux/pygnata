#!/usr/bin/env python
# -*- coding: utf-8 -*-

#The MIT License (MIT)
#Copyright (c) 2015 Alexandre LM, Dimitri S


import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(levelname)s]  %(message)s')

# Create an handler to show the logs in the consol
steam_handler = logging.StreamHandler()
steam_handler.setFormatter(formatter)
steam_handler.setLevel(logging.DEBUG)
logger.addHandler(steam_handler)

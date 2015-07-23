# -*- coding: utf-8 -*-

#The MIT License (MIT)
#Copyright (c) 2015 Alexandre LM, Dimitri S

from path import path
from .logger import logger


class PygnataProcessor(object):
    """
        Process a .pyg file
    """
    def __init__(self):
        #Part to process in a .pygnata file
        self.to_process = {'TREE': self.create_tree, }

    def process(self, root_path, part_dic):
        """
            Apply function for the part to process

            :param root_path: The absolute path of the .pyg file
            :param part_dic: The dict containing the parts informations

            :type root_path: string
            :type part_dic: dict

        """
        #Browse the part
        for part, content in list(part_dic.items()):
            #If it is a part to process
            if part in self.to_process:
                self.to_process[part](root_path, part_dic[part])

    def create_tree(self, root_path, tree_lst):
        """
            Generate a folder tree recurcively

            :param root_path: The path use to generate the tree
            :param tree_array: The list containing the TREE part informations

            :type root_path: string
            :type tree_array: list

        """
        root = path(root_path)

        #Browse the tree array
        for value in tree_lst:
            #if it is a dict
            if isinstance(value, dict):
                for key, value in list(value.items()):
                    #Create the new root Path
                    new_path = root / key
                    new_path.mkdir()
                    logger.info("New dir  {}".format(new_path))
                    #Call the function recursively
                    self.create_tree(new_path, value)
            #If not a dict, create the file
            else:
                new_file = root / value
                new_file.touch()
                logger.info("New file {}".format(new_file))

# -*- coding: utf-8 -*-

#The MIT License (MIT)
#Copyright (c) 2015 Alexandre LM, Dimitri S

import time
import yaml
import re

from path import path
from jinja2 import Environment
from .config.config import pygconfig
from .exception import BuilderError
from .logger import logger


class PygnataBuilder(object):
    """
        Class use for build a pygnata file
    """
    def __init__(self):

        #Get the file extension for the built files
        self.extension = pygconfig.get('BUILDER', 'Extension')

        #Get the default folder for the built files
        self.build_dir = path(pygconfig.get('BUILDER', 'DefaultBuildDir'))
        self.build_dir = self.build_dir.expand()

        #Get the template with the structure of a .pyg file
        template_path = path(pygconfig.get('BUILDER', 'TemplateFile'))
        self.template = path(__file__).parent / template_path

        #Associate a function to a field of the .pyg template
        self.fields = {pygconfig.get('BUILDER', 'DateField'): self.get_date,
                       pygconfig.get('BUILDER', 'TreeField'): self.get_tree}

        #Get the pattern for the date in the template file
        self.date_pattern = path(pygconfig.get('BUILDER', 'DateFormat'))

    def build(self, src_folder, dst=None, out_name=None, ignored=None):
        """
            Build a .pyg file base on an existing directory

            :param src_folder: The absolute path of the root folder
            :param dst: The destination path of the built .pyg file
            :param out_name: The custom name for the built .pyg file
            :param ignored: Regex list for ignored files/folder

            :type src_folder: string
            :type dst: string
            :type out_name: string
            :type ignored: list

            :return: The absolute path of the built .pyg file
            :rtype: string

        """
        src_path = path(src_folder).expand()

        #Set the name of the destination file
        dest_name = src_path.name + self.extension

        #Set the default destination folder for the built .pyg file
        dest_folder = self.build_dir

        #Set the destination folder
        if dst and path(dst).isdir():
            dest_folder = path(dst)
        else:
            if dst is not None:
                raise BuilderError("{} is not a directory".format(dst))

        #Compile regex list for ignored files/folders
        if ignored:
            ignored = [re.compile(regex) for regex in ignored]

        #If provided, set the new name of the .pyg file
        if out_name:
            if not out_name.endswith(self.extension):
                out_name = out_name + self.extension
            dest_name = path(out_name)

        #Set the path of the destination file
        dest_path = dest_folder / dest_name

        #Open the template defining the .pyg file
        with open(self.template, 'r') as fd:
            template = fd.read()

            #browse the field list and launch the appropriate function
            for field, funct in list(self.fields.items()):
                ret = funct(src_folder, ignored)
                self.fields[field] = ret

            #Replace the value in template with jinja
            new_template = Environment().from_string(template)
            new_template = new_template.render(self.fields)

            #open the destination file and write the new template inside
            with open(dest_path, 'w') as cd:
                cd.write(str(new_template))

        #return the absolute path of the .pyg file
        return dest_path

    def get_date(self, *options):
        """
            Generate a formated string of the current time

            :param options: A list of optionnal arguments

            :type options: list

            :return: The current time formatted
            :rtype: string
        """
        #Get the current date
        return time.strftime(self.date_pattern)

    def get_tree(self, src_folder, ignored):
        """
            Create and return a Yaml tree of a folder

            :param src_folder: The root folder of the tree
            :param ignored: A list of regex use to ignore files and folders

            :type src_folder: string
            :type ignored: list

            :return: A YAML folder tree
            :rtype: string
        """
        tree_list = []

        #Get the absolute path of the src_folder
        abs_path = path(src_folder).abspath()

        #If the folder doesn't exist
        if not abs_path.exists():
            raise BuilderError("File {} unknown".format(abs_path))

        #Set the root path
        root_path = abs_path

        #Get the tree
        tree_list.append(self.generate_tree_dict(root_path, ignored))

        #Return a Yaml format of the tree
        return yaml.dump(tree_list, default_flow_style=False)

    def generate_tree_dict(self, root_path, ignored):
        """
            Generate a dict of a folder and sub folders from a root path.

            :param root_path: The root folder of the folder tree
            :param ignored: A list of regex use to ignore files and folders

            :type root_path: string
            :type ignored: list

            :return: A dict representing a folder tree
            :rtype: dic
        """

        tree_dic = {}

        #Initiate the dict with the root path
        tree_dic[str(root_path.name)] = []

        #If the root_path is just a file
        if not root_path.isfile():
            #For each dir/file in root_path
            for objects in root_path.listdir():
                #If the object name is in the exclusion list
                if not self.match_with_regex(objects.name, ignored):
                    if objects.isfile():
                        #Add in folder array for the root path
                        tree_dic[str(root_path.name)].append(str(objects.name))

                    if objects.isdir():
                        tmp_dir = {}
                        #Call generate_tree_dict recursively
                        tmp_dir = self.generate_tree_dict(objects, tmp_dir, ignored)
                        tree_dic[str(root_path.name)].append(tmp_dir)

        return tree_dic

    def match_with_regex(self, input, ignored_lst):
        """
            Test if a string match with a list of regex

            :param input: The string to test
            :param ignored_lst: A list of regex use to ignore files and folders

            :type input: string
            :type ignored_lst: list

            :return: If the name match with a regex
            :rtype: bool
        """
        if ignored_lst:
            for regex in ignored_lst:
                #If only one match it's done
                if regex.match(input):
                    return True
        return False

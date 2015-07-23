# -*- coding: utf-8 -*-

#The MIT License (MIT)
#Copyright (c) 2015 Alexandre LM, Dimitri S

import os.path
import re
import yaml

from jinja2 import Environment

from .config.config import pygconfig
from .exception import ParserError
from .logger import logger


class PygnataParser(object):
    """
        Class use to parse a .pyg file
    """

    def __init__(self):

        #Get the parts name
        self.var_part = pygconfig.get('GENERAL', 'VarPart')
        self.static_part = pygconfig.get('GENERAL', 'StaticPart')
        self.tree_part = pygconfig.get('GENERAL', 'TreePart')
        self.info_part = pygconfig.get('GENERAL', 'InfoPart')

        #Get the require part
        self.req_parts = pygconfig.get('PARSER', 'RequirePart').split(',')
        #Get all the parts of a pyg file
        self.all_parts = pygconfig.get('PARSER', 'AllPart').split(',')

        #Get required fields for the info part
        info_field = pygconfig.get('PARSER', 'InfoFields').split(',')
        self.req_fields = {self.info_part: info_field}

    def parse(self, absolute_path, ask_var=True):
        """
            Parse a Pygnata file and return a dictionnary with
            the part name as key and the part content as value.

            :param absolute_path: The absolute path of the .pyg file
            :param ask_var: Indicate if the the VAR part should be processed

            :type absolute_path: string
            :type ask_var: bool

            :return: The dict containing the parts and related informations
            :rtype: dict
        """
        if not os.path.isfile(absolute_path):
            raise ParserError("The file does not exist")

        part_dic = None

        with open(absolute_path, 'r') as fd:

            #retireve the parts
            part_dic = self.get_parts(fd.read())

            #browse the part and convert the content with Yaml
            #except the tree part
            for part, content in list(part_dic.items()):
                #If it is not the tree part and the part is not empty
                if part != self.tree_part:
                    yml_content = yaml.load(content[0])

                    #If it is the VAR part and if it is not the show function,
                    # we ask for user values
                    if part == self.var_part and ask_var:
                        yml_content = self.ask_variable(yml_content)

                    part_dic[part] = yml_content

                #Test the required fields
                self.test_required_fields(part, part_dic[part])

            #Replace variable in tree with jinja2
            tree = part_dic[self.tree_part][0]

            #Get None if var or static are absents
            var = part_dic.get(self.var_part)
            static = part_dic.get(self.static_part)

            part_dic[self.tree_part] = self.generate_tree(tree, var, static)

        return part_dic

    def get_parts(self, file_content):
        """
            Retrieve the diffrent parts of the pygnata file
            and return a dic with part name as key and content
            as value (JinJa/YAML).

            :param file_content: The raw content of the .pyg file

            :type file_content: string

            :return: The dict containing the parts and related informations
            :rtype: dict
        """
        part_dic = {}

        #get the main parts
        parts = [_f for _f in re.split('---\n', file_content) if _f]

        #Browse all parts
        for one_part in parts:
            #retrieve the part title
            content = [x for x in re.split("^([A-Z]+):\n", one_part) if x]
            #Get the part title
            part_title = content[0]

            #Test if this part is allowed
            if part_title and part_title not in self.all_parts:
                raise ParserError("Unknown part {}".format(part_title))

            #Add the part and is content without the part title and \n
            #in the dictionnary
            part_dic[part_title] = content[1:]

        #Test if all required part are present
        for parts in self.req_parts:
            if parts not in part_dic:
                raise ParserError("Part {} required".format(parts))

        return part_dic

    def test_required_fields(self, part, content):
        """
            Test if all required field are present in a required part

            :param part: The current part name
            :param content: The content of the part

            :type part: string
            :type content: dict

        """
        #If part is in res_fields dict
        if part in self.req_fields:
            #Get the required fields
            required = self.req_fields[part]
            for field in required:
                #If the field is absent
                if field not in content:
                    raise ParserError("{}- Field {} absent".format(part, field))

    def generate_tree(self, tree, variable, static):
        """
            Generate a YAML tree by replacing Jinja variable by
            the value from VAR and STATIC part.

            :param tree: The folder tree with Jinja2 variables
            :param variable: The variable content dict
            :param static: The static content dict

            :type tree: string
            :type variable: dict
            :type static: dict

            :return: The YAML folder tree
            :rtype: string
        """
        #Concat the static and var part
        jinja_var = {}
        if variable:
            jinja_var.update(variable)
        if static:
            jinja_var.update(static)

        #Generate Tree
        new_tree = Environment().from_string(tree).render(jinja_var)

        #generate yaml tree
        return yaml.load(new_tree)

    def ask_variable(self, var_dic):
        """
            Get the VAR part values by asking the user.

            :param var_dic: The dic containing the VAR part fields

            :type var_dic: dict

            :return: The VAR part dict with the user answer
            :rtype: dict
        """
        #If VAR part dict is not empty
        if var_dic:
            logger.info("Pygnata need some informations:")

            #Ask user for variable
            for var, msg in list(var_dic.items()):
                to_print = "\t(?) - {} ? : ".format(msg)
                var_in = input(to_print)

                while var_in.replace(" ", "") is "":
                    logger.error(" (!) you should answer something!")
                    var_in = input(to_print)

                tab_var = var_in.split(",")
                var_dic[var] = var_in if len(tab_var) <=1 else tab_var 

            return var_dic

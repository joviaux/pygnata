# -*- coding: utf-8 -*-

#The MIT License (MIT)
#Copyright (c) 2015 Alexandre LM, Dimitri S

from .config.config import pygconfig
from path import path


class PygnataDisplay(object):
    """
        Class used to display various informations about a .pyg file
    """

    def __init__(self):
        #Associate the print function to each part
        self.parts_fcn = {pygconfig.get('GENERAL', 'InfoPart'): self.print_part,
                      pygconfig.get('GENERAL', 'VarPart'): self.print_part,
                      pygconfig.get('GENERAL', 'StaticPart'): self.print_part,
                      pygconfig.get('GENERAL', 'TreePart'): self.print_tree}

        #Get the parts to display
        self.to_print = pygconfig.get('DISPLAY', 'ToPrint').split(',')

    def show(self, part_dic):
        """
            Function that show all the parts

            :param part_dic: The dict containing informations about the parts

            :type part_dic: dict
        """
        #Browse the parts
        for part in sorted(part_dic):
            #if the part is in parts dict and is in the to_print dict
            if part in self.parts_fcn and part in self.to_print:
                #Call the function associated to the part
                self.parts_fcn[part](part, part_dic[part])
        print()

    def print_part(self, part, info_dic):
        """
            Print a regular part

            :param part: The part name
            :param info_dic: The part content

            :type part: string
            :type info_dic: dict
        """
        #if part isn't empty
        if info_dic:
            print(("\n────────────[{} PART]────────────\n".format(part)))
            #Browse the part content
            for key, value in sorted(list(info_dic.items())):
                print(("<{}> ─ {}".format(key, value)))

    def print_tree(self, part, tree_dic):
        """
            Print the content of the tree part

            :param part: The part name
            :param tree_dic: The dict containing the (sub)folders of the tree

            :type part: string
            :type tree_dic: dict
        """
        #If the tree isn't empty
        if tree_dic:
            print()
            print(("────────────[{} PART]────────────\n".format(part)))
            self.print_recursive_tree("", tree_dic)

    def print_recursive_tree(self, root_path, tree_dic):
        """
            Print a folder tree recurcively

            :param root_path: The root path of the tree
            :param tree_dic: The dict containing the (sub)folders of the tree

            :type root_path: string
            :type tree_dic: dict
        """
        root = path(root_path)

        #Browse the tree array
        for index, value in enumerate(tree_dic):

            #if it is a sub folder
            if isinstance(value, dict):
                for key, value in list(value.items()):

                    #Create the new root path
                    new_path = root / key

                    #If it is not the first folder
                    if new_path.parent:
                        #Begin the line with a pipe
                        print("│", end="")  # lint:ok

                        #If it is the last line
                        if index == (len(tree_dic) - 1):
                            print("  └── {}".format(new_path.name))
                        else:
                            print("  ├── {}".format(new_path.name))

                    else:
                        #redefine the root
                        print("{}".format(new_path.name))

                    #call print_recursive_tree recursively
                    self.print_recursive_tree(new_path, value)

            #If not a sub folder, create the file
            else:

                #Define the new file path
                new_file = root / value

                #If the file is the child of the main folder
                if new_file.parent.parent:
                    #Begin the line with a pipe
                    print("│", end="")

                    #If it is the last line
                    if index == (len(tree_dic) - 1):
                        print("     └── {}".format(new_file.name))
                    else:
                        print("     ├── {}".format(new_file.name))
                else:
                    #If it is the last line
                    if index == (len(tree_dic) - 1):
                        print("└── {}".format(new_file.name))
                    else:
                        print("├── {}".format(new_file.name))

# -*- coding: utf-8 -*-

#The MIT License (MIT)
#Copyright (c) 2015 Alexandre LM, Dimitri S

"""That script.
Usage:
  pygnata (-h|--help)
  pygnata [-l <value> | --local <value>]
  pygnata [-u <value> | --url <value>]
  pygnata [-d <value> | --database <value>]
  pygnata <src>
  pygnata create <src> [<dest>] [--ignore ... | -i ...] [-o <filename> | --output <filename>]
  pygnata show <src>
  pygnata show [-l <value> | --local <value>]
  pygnata show [-u <value> | --url <value>]
  pygnata show [-d <value> | --database <value>]
  pygnata save <src> [<dest>]
  pygnata save [-l <value> | --local <value>] [<dest>]
  pygnata save [-u <value> | --url <value>] [<dest>]
  pygnata save [-d <value> | --database <value>] [<dest>]

Options:
  -h --help  Show this help message and exit
  -o <filename>, --output <filename>  Specify an output name for .pyg file
  -u <url>, --url <url>  Get .pyg file from URL.
  -d <filename>, --database <filename>  Get .pyg file from the database.
  -i ..., --ignore ... Files/folders to ignore when creating .pyg file
"""

from .provider import PygnataProvider
from .parser import PygnataParser
from .processor import PygnataProcessor
from .display import PygnataDisplay
from .builder import PygnataBuilder
from .logger import logger
from .exception import ParserError, BuilderError, ProviderError

__all__ = ['pygnata_run']

from docopt import docopt


# Initialize pygnata
pyg_provider = PygnataProvider()
pyg_parser = PygnataParser()
pyg_proc = PygnataProcessor()
pyg_display = PygnataDisplay()
pyg_builder = PygnataBuilder()


def pygnata_save(provide_type, src, dest=None, *options):
    """
        Save a pygnata file in .pygnata folder or in a custom path

        :param provide_type: The providing method choose to retrieve the file
        :param src: The value provided in the command line
        :param dest: The destination provided in the command line
        :param options: A list containing the unused options

        :type provide_type: int
        :type src: string
        :type dest: string
        :type options: list
    """
    file_path = pyg_provider.search(provide_type, src)

    if pyg_parser.parse(file_path, False):
        logger.info(" The file seems to be OK :D")
        #Put the file in the .pygnata folder
        location = pyg_provider.put_to_local(file_path, dest)
        logger.info((" File saved in {}".format(location)))


def pygnata_build(provide_type, src, dest=None, out_name=None, ignored=None):
    """
        Generate a pygnata file from an existing folder

        :param provide_type: The providing method choose to retrieve the file
        :param src: The value provided in the command line
        :param dest: The destination provided in the command line
        :param out_name: The output name provided in the command line
        :param ignored: A list of regex used for ignoring files or folders

        :type provide_type: int
        :type src: string
        :type dest: string
        :type out_name: string
        :type ignored: list
    """
    logger.info((" Building the file from folder {}".format(src)))
    #Build the template
    path = pyg_builder.build(src, dest, out_name, ignored)
    logger.info((" File built in {}".format(path)))


def pygnata_install(provide_type, src, *options):
    """
        Generate the project tree from a .pyg file

        :param provide_type: The providing method choose to retrieve the file
        :param src: The value provided in the command line
        :param options: A list containing the unused options

        :type provide_type: int
        :type src: string
        :type options: list
    """
    file_path = pyg_provider.search(provide_type, src)
    logger.info((" Generate from file \"{}\" --".format(file_path)))
    file_dic = pyg_parser.parse(file_path)

    logger.info((" Parse file \"{}\" --".format(file_path)))
    pyg_proc.process("./", file_dic)


def pygnata_show(provide_type, src, *options):
    """
        Show the content of a .pyg file

        :param provide_type: The providing method choose to retrieve the file
        :param src: The value provided in the command line
        :param options: A list containing the unused options

        :type provide_type: int
        :type src: string
        :type options: list
    """
    file_path = pyg_provider.search(provide_type, src)
    logger.info((" Informations from file \"{}\" --".format(file_path)))
    file_dic = pyg_parser.parse(file_path, False)
    #Print the file content
    pyg_display.show(file_dic)


def pygnata_run():
    """
        Entry point of Pygnata
    """
    arguments = docopt(__doc__, version='0.1')

    #Get the pygnata main functions
    functions = {'save': pygnata_save,
                 'show': pygnata_show,
                 'create': pygnata_build}

    #Associate type to options
    types = {'--local': PygnataProvider.LOCAL,
             '--url': PygnataProvider.URL,
             '--database': PygnataProvider.DATABASE}

    #List the options
    src_file = "<src>"
    dst_file = "<dest>"
    type_value = "<value>"
    ignore = ["-i", "--ignore"]
    output = ["-o", "--output"]

    source = None
    destination = None

    # Install by default
    current_fct = pygnata_install
    is_ignored = None
    out_name = None

    # Set current by default
    current_type = PygnataProvider.CURRENT

    # Browse the command line options
    for option, value in list(arguments.items()):
        if value:
            # Get the function associated to the main option
            if option in functions:
                current_fct = functions[option]

            if option in types:
                current_type = types[option]
                source = value

            # If it's the value attached to a type
            if option == type_value:
                source = value

            if option == src_file:
                source = value

            if option in output:
                out_name = value

            if option in ignore:
                is_ignored = value.split(',')

            if option == dst_file:
                destination = value

    if not source and current_type == PygnataProvider.CURRENT:
        logger.error("Don't know how to use pygnata? Try 'pygnata -h' first!")
    else:
        try:
            # Execute the function with arg
            current_fct(current_type, source, destination, out_name, is_ignored)
        except ProviderError as e:
            logger.critical('ProviderError: {}'.format(e))
        except ParserError as e:
            logger.critical('ParserError: {}'.format(e))
        except BuilderError as e:
            logger.critical('BuilderError: {}'.format(e))
        except Exception as e:
            logger.error('UnknownError: {}'.format(e))

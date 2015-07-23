# -*- coding: utf-8 -*-

#The MIT License (MIT)
#Copyright (c) 2015 Alexandre LM, Dimitri S

import os.path
import shutil
import urllib.request
from .exception import ProviderError
from .logger import logger
from .config.config import pygconfig
from .logger import logger
from path import path


class PygnataProvider(object):
    """
        Class used to retrieve a .pyg file from many locations
    """
    #Path for the local Pygnata files
    Pygnata_local_path = path(pygconfig.get('PROVIDER', 'AppDir')).expand()
    #Path for the tempory local Pygnata files
    Pygnata_tmp_path = path(pygconfig.get('PROVIDER', 'TmpAppDir')).expand()
    #Extension of the Pygnata files
    extension = pygconfig.get('PROVIDER', 'Extension')

    #Get the values for providing methods
    DATABASE = pygconfig.get('PROVIDER', 'Database')
    URL = pygconfig.get('PROVIDER', 'Url')
    LOCAL = pygconfig.get('PROVIDER', 'Local')
    CURRENT = pygconfig.get('PROVIDER', 'Current')

    def __init__(self):
        #Check if the local folder and tmp local folder exists
        #if not, they will be created.
        if not os.path.isdir(PygnataProvider.Pygnata_local_path):
            os.makedirs(PygnataProvider.Pygnata_local_path)

        if not os.path.isdir(PygnataProvider.Pygnata_tmp_path):
            os.makedirs(PygnataProvider.Pygnata_tmp_path)

    def search(self, provide_type, value):
        """
            Launch the proper providing function to retrieve a .pyg file.

            :param provide_type: The method number for retrieving .pyg file
            :param value: The value use to search the file

            :type provide_type: int
            :type value: string

            :return: The absolute path of the .pyg file
            :rtype:  Path

            .. note:: Local search is the default behavior
        """
        #Associate provinding method number to appropriate search function
        methods = {PygnataProvider.DATABASE: self.search_database,
                   PygnataProvider.URL: self.search_url,
                   PygnataProvider.LOCAL: self.search_local,
                   PygnataProvider.CURRENT: self.search_current}  # 3

        if not provide_type:
            #By default the CURRENT folder method
            provide_type = PygnataProvider.CURRENT

        #Call the proper method
        return methods[provide_type](value)

    def search_current(self, value):
        """
            Search in the current folder

            :param value: The value use to search the file

            :type value: string

            :return: The absolute path of the .pyg file
            :rtype:  Path
        """
        #Set the filename
        file_name = value

        #Check if the value arg don't end with .Pygnata
        if not value.endswith(PygnataProvider.extension):
            file_name = file_name + PygnataProvider.extension

        #Check if the file exist in the current directory
        current_folder = path.getcwd()
        local_pyg_files = os.listdir(current_folder)
        if file_name in local_pyg_files:
            return os.path.abspath(current_folder / path(file_name))
        else:
            #Search in the .pygnata folder
            return self.search_local(value)

    def search_database(self, value):
        """
            Search a file in an online database

            :param value: The value use to search the file

            :type value: string

            :return: The absolute path of the .pyg file
            :rtype:  Path

            .. warnings:: Function not implemented yet
        """
        logger.debug(("my value arg {}".format(value)))
        #SOOOON!
        pass

    def search_local(self, value):
        """
            Search a PygnataFile in the .pygnata directory

            :param value: The value use to search the file

            :type value: string

            :return: The absolute path of the .pyg file
            :rtype:  Path
        """
        #Set the filename
        file_name = value

        #Check if the value arg don't end with .Pygnata
        if not value.endswith(PygnataProvider.extension):
            file_name = file_name + PygnataProvider.extension

        #Check if the file exist in the .pygnata folder
        if not file_name in os.listdir(PygnataProvider.Pygnata_local_path):
            #We search for a path if local failed
            return self.search_path(value)
        else:
            #Set the path
            file_path = PygnataProvider.Pygnata_local_path / path(file_name)
            #return the absolute path and the neighbors files path
            return os.path.abspath(file_path)

    def search_path(self, value):
        """
            Search a PygnataFile from a specified path

            :param value: The specified path

            :type value: string

            :return: The absolute path of the .pyg file
            :rtype:  Path
        """
        #Use os.path.expanduser to avoid ~
        file_path = path(value).expanduser()
        #Check the file extension
        if not file_path.endswith(PygnataProvider.extension):
            raise ProviderError("Not a .pyg file")

        #Test if the path exist
        if not os.path.isfile(file_path):
            raise ProviderError("The file does not exist")

        #return the absolute path of the file
        return os.path.abspath(file_path)

    def search_url(self, value):
        """
            Search a PygnataFile from an URL

            :param value: The specified URL

            :type value: string

            :return: The absolute path of the .pyg file
            :rtype:  Path

            .. warnings:: Function not fully tested and functionnal
        """
        if not value:
            raise ProviderError("No URL provided")

        #Set the filenames
        original_name = value.split('/')[-1]
        file_name = original_name.split('.')[0] + PygnataProvider.extension
        tmp_filename = PygnataProvider.Pygnata_tmp_path + file_name + ".tmp"
        #final_filename = PygnataProvider.Pygnata_local_path + file_name

        #Open the URL
        response = urllib.request.urlopen(value)
        #Open the file
        with open(tmp_filename, 'wb') as fd:
            #get the file size
            file_size = int(response.getheader("Content-Length"))
            logger.info("Downloading: {}({} b)".format(tmp_filename, file_size))
            file_size_dl = 0
            block_sz = 8192
            while True:
                file_buffer = response.read(block_sz)
                #If nothing to read
                if not file_buffer:
                    break
                #Copy data in the buffer
                file_size_dl += len(file_buffer)
                #Copy the buffer in the file
                fd.write(file_buffer)
                #Calculate the ddl percent
                ddl_percent = (file_size_dl / file_size) * 100
                status = r"%10d [%3.2f%%]" % (file_size_dl, ddl_percent)
                print(status)

        #If the file is ok, we put in .Pygnata file
        #os.rename(tmp_filename, final_filename)

        #return the abs path of the tmp file
        return os.path.abspath(tmp_filename)

    def put_to_local(self, absolute_path, name=None):
        """
            Put a copy of a .pyg file in the .pygnata folder

            :param absolute_path: The absolute path of the source file
            :param name: The new name of the file

            :type absolute_path: string
            :type name: string

            :return: The absolute path of the .pyg file
            :rtype:  Path

            .. warnings:: Function not fully tested and functionnal
        """
        local_path = PygnataProvider.Pygnata_local_path
        #Set the original filename
        file_name = absolute_path.split("/")[-1]
        #If there is a custom name
        if name:
            #If the extension is here
            if name.endswith(PygnataProvider.extension):
                file_name = name
            else:
                file_name = name + PygnataProvider.extension
        #Set the destination path
        dest = local_path / path(file_name)

        #If the file already exist
        if dest.exists():
            logger.info("File already exist in {}, replace? (Y/n)".format(local_path))
            value = str(input())

            while value is not "Y" and value is not "n":
                logger.info("File already exist in {}, replace? (Y/n)".format(local_path))
                value = str(input())

            if value is "Y":
                #copy the src to dest
                shutil.copy2(absolute_path, dest)
                #return the absolute path
                return os.path.abspath(dest)

        logger.info("Copy in {} folder abort!".format(local_path))
        return absolute_path

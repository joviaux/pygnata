# -*- coding: utf-8 -*-

#The MIT License (MIT)
#Copyright (c) 2015 Alexandre LM, Dimitri S

class ProviderError(Exception):
    """Exception raised for errors in the provider class.

    Attributes:
        value -- explanation of the error
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class ParserError(Exception):
    """Exception raised for errors in the parser class.

    Attributes:
        value -- explanation of the error
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class BuilderError(Exception):
    """Exception raised for errors in the builder class.

    Attributes:
        value -- explanation of the error
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

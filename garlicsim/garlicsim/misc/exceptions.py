# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines a collection of exceptions.'''


class SmartException(Exception):
    '''
    Exception that uses its first line of documentation in lieu of a message.
    '''
    def __init__(self, msg=None):
        if msg is None:
            if self.__doc__:
                msg = self.__doc__.strip().split('\n')[0] 
                # Getting the first line of the documentation
        Exception.__init__(self, msg)


class GarlicSimException(SmartException):
    '''GarlicSim-related exception.'''

class GarlicSimWarning(Warning):
    '''GarlicSim-related warning.'''
    

class InvalidSimpack(GarlicSimException):
    '''Trying to load an invalid simpack.'''

class SimpackError(GarlicSimException):
    '''A simpack behaved unexpectedly.'''

    
    
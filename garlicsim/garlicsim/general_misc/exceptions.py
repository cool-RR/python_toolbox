# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines exceptions.'''

from third_party import abc


class CuteException(Exception):
    '''
    Exception that uses its first line of documentation in lieu of a message.
    '''

    __metaclass__ = abc.ABCMeta


    def __init__(self, msg=None):
        # We use `None` as the default for `msg`, so the user can input '' to
        # force an empty message.
        
        if type(self) is CuteException:
            raise Exception('''You tried to create a CuteException instance, \
but the CuteException class is meant to be used as a base class for \
exceptions, and it can't be raised by itself.''')
        
        if msg is None:
            if self.__doc__:
                msg = self.__doc__.strip().split('\n')[0] 
                # Getting the first line of the documentation
            else:
                msg = ''
                
        Exception.__init__(self, msg)

        
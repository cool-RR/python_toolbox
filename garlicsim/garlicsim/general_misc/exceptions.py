# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines exceptions.'''


class CuteException(Exception):
    '''
    Exception that uses its first line of documentation in lieu of a message.
    '''

    def __init__(self, msg=None):
        # We use `None` as the default for `msg`, so the user can input '' to
        # force an empty message.
        
        if msg is None:
            if self.__doc__ and (type(self) is not CuteException):
                msg = self.__doc__.strip().split('\n')[0] 
                # Getting the first line of the documentation
            else:
                msg = ''
                
        Exception.__init__(self, msg)

        
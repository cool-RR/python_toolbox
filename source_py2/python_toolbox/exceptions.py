# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines exceptions.'''


class CuteBaseException(BaseException):
    '''
    Base exception that uses its first docstring line in lieu of a message.
    '''

    def __init__(self, message=None):
        # We use `None` as the default for `message`, so the user can input ''
        # to force an empty message.
        
        if message is None:
            if self.__doc__ and \
                        (type(self) not in (CuteBaseException, CuteException)):
                message = self.__doc__.strip().split('\n')[0] 
                # Getting the first line of the documentation
            else:
                message = ''
                
        BaseException.__init__(self, message)
        
        self.message = message
        '''
        The message of the exception, detailing what went wrong.
        
        We provide this `.message` attribute despite `BaseException.message`
        being deprecated in Python. The message can also be accessed as the
        Python-approved `BaseException.args[0]`.
        '''
        

class CuteException(CuteBaseException, Exception):
    '''Exception that uses its first docstring line in lieu of a message.'''
    

        
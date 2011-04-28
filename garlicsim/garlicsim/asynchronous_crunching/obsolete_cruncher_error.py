# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `ObsoleteCruncherException` exception.

See its documentation for more info.
'''

class ObsoleteCruncherException(BaseException):
    '''
    The cruncher that got this exception raised became obsolte.
    
    The cruncher is trying to do work, but in the meantime the main program
    decided that the work assigned to this cruncher is no longer wanted, and
    should therefore be stopped.
    '''
    # Inherits from BaseException because it is an exit exception    
    # todo: I heard that `BaseException.message` is deprecated! Problematic?
    # Maybe make `CuteBaseException`?

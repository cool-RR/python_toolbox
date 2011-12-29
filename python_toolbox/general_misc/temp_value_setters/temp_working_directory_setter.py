# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `TempWorkingDirectorySetter` class.

See its documentation for more details.
'''

import os

from .temp_value_setter import TempValueSetter


class TempWorkingDirectorySetter(TempValueSetter):
    '''
    Context manager for temporarily changing the working directory.
    
    The temporary working directory is set before the suite starts, and the
    original working directory is used again after the suite finishes.
    '''
    def __init__(self, working_directory):
        '''
        Construct the `TempWorkingDirectorySetter`.
        
        `working_directory` is the temporary working directory to use.
        '''
        assert isinstance(working_directory, basestring)
        TempValueSetter.__init__(self,
                                 (os.getcwd, os.chdir),
                                 value=working_directory)
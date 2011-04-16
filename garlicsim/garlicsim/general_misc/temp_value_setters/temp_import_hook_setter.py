# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `TempWorkingDirectorySetter` class. blocktododoc

See its documentation for more details.
'''

import __builtin__

from .temp_value_setter import TempValueSetter


class TempImportHookSetter(TempValueSetter):
    '''
    Context manager for temporarily changing the working directory. blocktododoc
    
    The temporary working directory is set before the suite starts, and the
    original working directory is used again after the suite finishes.
    '''
    def __init__(self, import_hook):
        '''
        Construct the `TempWorkingDirectorySetter`. blocktododoc
        
        `working_directory` is the temporary working directory to use.
        '''
        assert callable(import_hook)
        TempValueSetter.__init__(self,
                                 (__builtin__, '__import__'),
                                 value=import_hook)
# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''
Defines the `TempImportHookSetter` class.

See its documentation for more details.
'''

import builtins

from .temp_value_setter import TempValueSetter
import collections


class TempImportHookSetter(TempValueSetter):
    '''
    Context manager for temporarily setting a function as the import hook.
    '''
    def __init__(self, import_hook):
        '''
        Construct the `TempImportHookSetter`.
        
        `import_hook` is the function to be used as the import hook.
        '''
        assert callable(import_hook)
        TempValueSetter.__init__(self,
                                 (__builtin__, '__import__'),
                                 value=import_hook)
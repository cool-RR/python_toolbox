# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `MockImporter` class.

See its documentation for more information.
'''

import __builtin__

from garlicsim.general_misc.third_party import mock as mock_module


class MockImporter(object):
    '''
    Importer that creates a mock object instead of actually importing modules.
    '''
    
    def __init__(self, skip_first_import=False):
        '''
        Create the `MockImporter`.
        
        `skip_first_import` determines whether to skip the first `import`
        action, using the original import function for it.
        '''
        
        self.original_import = __builtin__.__import__
        '''The original `import` function that we're replacing.'''
        
        self.skip_first_import = skip_first_import
        '''Whether the first `import` should be skipped.'''
        
        self.times_called = 0
        '''How many times we were called to import.'''
        
        
    def __call__(self, name, globals={}, locals={}, fromlist=[], level=-1):
        '''Mock-import a module.'''
        if self.skip_first_import and self.times_called == 0:
            self.times_called = 1
            return self.original_import(name, globals, locals,
                                        fromlist, level)
        else:
            self.times_called += 1
            return mock_module.Mock(name=name)


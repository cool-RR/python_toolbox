# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `DelegateeContextManager` class.

See its documentation for more information.
'''

from garlicsim.general_misc import context_managers


class DelegateeContextManager(context_managers.ReentrantContextManager):
    '''
    
    
    '''
    def __init__(self, freezer):
        self.freezer = freezer
        
    def reentrant_enter(self):
        ''' '''
        return self.freezer.freeze_handler()
    
    def reentrant_exit(self, type_, value, traceback):
        ''' '''
        return self.freezer.thaw_handler()
        
    
# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `DelegateeContextManager` class.

See its documentation for more information.
'''

from garlicsim.general_misc import context_managers


class DelegateeContextManager(context_managers.ReentrantContextManager):
    '''Inner context manager used internally by `Freezer`.'''
    
    def __init__(self, freezer):
        '''
        Construct the `DelegateeContextManager`.
        
        `freezer` is the freezer to which we belong.
        '''
        self.freezer = freezer
        '''The freezer to which we belong.'''
        

    def reentrant_enter(self):
        '''Call the freezer's freeze handler.'''
        return self.freezer.freeze_handler()
    
    
    def reentrant_exit(self, exc_type, exc_value, exc_traceback):
        '''Call the freezer's thaw handler.'''
        return self.freezer.thaw_handler()
        
    
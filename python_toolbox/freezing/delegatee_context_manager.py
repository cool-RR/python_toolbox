# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import misc_tools
from python_toolbox import context_management


@context_management.as_reentrant
class DelegateeContextManager(context_management.ContextManager):
    '''Inner context manager used internally by `Freezer`.'''

    def __init__(self, freezer):
        '''
        Construct the `DelegateeContextManager`.

        `freezer` is the freezer to which we belong.
        '''
        self.freezer = freezer
        '''The freezer to which we belong.'''


    def __enter__(self):
        '''Call the freezer's freeze handler.'''
        return self.freezer.freeze_handler()


    def __exit__(self, exc_type, exc_value, exc_traceback):
        '''Call the freezer's thaw handler.'''
        return self.freezer.thaw_handler()

    depth = misc_tools.ProxyProperty('.__wrapped__.depth')

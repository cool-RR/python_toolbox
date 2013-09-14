# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''
This module defines the `BlankContextManager` class.

See its documentation for more information.
'''

from .context_manager import ContextManager


class BlankContextManager(ContextManager):
    '''A context manager that does nothing.'''
    def manage_context(self):
        yield self

# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `BlankContextManager` class.

See its documentation for more information.
'''

from .context_manager import ContextManager


class BlankContextManager(ContextManager):
    '''A context manager that does nothing.'''
    def manage_context(self):
        yield self

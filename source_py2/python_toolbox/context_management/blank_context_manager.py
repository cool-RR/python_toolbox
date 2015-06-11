# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

from .context_manager import ContextManager


class BlankContextManager(ContextManager):
    '''A context manager that does nothing.'''
    def manage_context(self):
        yield self

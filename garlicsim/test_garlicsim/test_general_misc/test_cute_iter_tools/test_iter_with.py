# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing module for `cute_iter_tools.iter_with`.'''

import itertools

from garlicsim.general_misc import context_managers

from garlicsim.general_misc.cute_iter_tools import iter_with


class MyContextManager(context_managers.ContextManager):
    def __init__(self):
        self.counter = -1
        self.active = False
    def manage_context(self):
        self.active = True
        self.counter += 1
        try:
            yield self
        finally:
            self.active = False
        

def test():
    '''Test the basic workings of `iter_with`.'''
    
    active_context_manager = MyContextManager()
    inactive_context_manager = MyContextManager()
    
    iterator = iter_with(range(5), active_context_manager)
    
    for i, j in itertools.izip(iterator, range(5)):
        assert i == j == active_context_manager.counter
        assert active_context_manager.active is False
        assert inactive_context_manager.counter == -1
        assert inactive_context_manager.active is False
        
    
# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `cute_iter_tools.iter_with`.'''

import itertools

from python_toolbox import nifty_collections
from python_toolbox import context_management

from python_toolbox.cute_iter_tools import iter_with


class MyContextManager(context_management.ContextManager):
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
    
    iterator = iter_with(xrange(5), active_context_manager)
    
    for i, j in itertools.izip(iterator, xrange(5)):
        assert i == j == active_context_manager.counter
        assert active_context_manager.active is False
        assert inactive_context_manager.counter == -1
        assert inactive_context_manager.active is False
        
def test_lazy_tuple():
    
    active_context_manager = MyContextManager()
    inactive_context_manager = MyContextManager()
    
    lazy_tuple = iter_with(range(5), active_context_manager, lazy_tuple=True)
    assert isinstance(lazy_tuple, nifty_collections.LazyTuple)
    assert not lazy_tuple.collected_data
    
    for i, j in itertools.izip(lazy_tuple, range(5)):
        assert i == j == active_context_manager.counter
        assert active_context_manager.active is False
        assert inactive_context_manager.counter == -1
        assert inactive_context_manager.active is False
        
    assert lazy_tuple[2] == 2
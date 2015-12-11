# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `context_management.ReentrantContextManager`.''' 

import queue as queue_module

from python_toolbox.context_management import idempotentify, ContextManager
from python_toolbox import cute_testing


class SomeContextManager(ContextManager):
    x = 0
    def manage_context(self):
        self.x += 1
        try:
            yield self
        finally:
            self.x -= 1
            
            

def test_idempotentify():
    some_context_manager = SomeContextManager()
    assert some_context_manager.x == 0
    with some_context_manager:
        assert some_context_manager.x == 1
    assert some_context_manager.x == 0
    
    some_context_manager.__enter__()
    assert some_context_manager.x == 1
    some_context_manager.__enter__()
    assert some_context_manager.x == 2
    some_context_manager.__enter__()
    assert some_context_manager.x == 3
    some_context_manager.__exit__(None, None, None)
    assert some_context_manager.x == 2
    some_context_manager.__exit__(None, None, None)
    assert some_context_manager.x == 1
    some_context_manager.__exit__(None, None, None)
    assert some_context_manager.x == 0
    with cute_testing.RaiseAssertor():
        some_context_manager.__exit__(None, None, None)
    with cute_testing.RaiseAssertor():
        some_context_manager.__exit__(None, None, None)
        
    idempotent_context_manager = idempotentify(SomeContextManager())

    idempotent_context_manager.__enter__()
    assert idempotent_context_manager.__wrapped__.x == 1
    idempotent_context_manager.__enter__()
    assert idempotent_context_manager.__wrapped__.x == 1
    idempotent_context_manager.__enter__()
    assert idempotent_context_manager.__wrapped__.x == 1
    idempotent_context_manager.__exit__(None, None, None)
    assert idempotent_context_manager.__wrapped__.x == 0
    idempotent_context_manager.__exit__(None, None, None)
    assert idempotent_context_manager.__wrapped__.x == 0
    idempotent_context_manager.__exit__(None, None, None)
    assert idempotent_context_manager.__wrapped__.x == 0
    
        
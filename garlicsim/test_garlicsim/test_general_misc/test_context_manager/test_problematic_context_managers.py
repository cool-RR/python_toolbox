# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing module for various problematic context managers.'''

import nose

from garlicsim.general_misc import cute_testing

from garlicsim.general_misc.context_manager import (ContextManager,
                                                    ContextManagerType,
                                                    SelfHook)

def test_defining_enter_and_manage_context():
    
    with cute_testing.RaiseAssertor(
        Exception,
        'both an `__enter__` method and a'
        ):
        
        class MyContextManager(ContextManager):
            def manage_context(self):
                yield self
            def __enter__(self):
                return self

            
def test_defining_exit_and_manage_context():
    
    with cute_testing.RaiseAssertor(
        Exception,
        'both an `__exit__` method and a'
        ):
        
        class MyContextManager(ContextManager):
            def manage_context(self):
                yield self
            def __exit__(self):
                return self
            


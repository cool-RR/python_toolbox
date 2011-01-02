# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

from __future__ import with_statement

import nose

from garlicsim.general_misc.context_manager import (ContextManager,
                                                    ContextManagerType,
                                                    SelfHook)

def test_abstractness():
    
    def f():
        class EmptyContextManager(ContextManager):
            pass
    
    def g():
        class EnterlessContextManager(ContextManager):
            def __exit__(self, type_, value, traceback):
                pass
    
    def h():
        class ExitlessContextManager(ContextManager):
            def __enter__(self):
                pass
        
    nose.tools.assert_raises(TypeError, f)
    nose.tools.assert_raises(TypeError, g)
    nose.tools.assert_raises(TypeError, h)
    
    class MyContextManager(ContextManager):
        def manage_context(self):
            yield self
    
    class AnotherContextManager(ContextManager):
        def __enter__(self):
            pass
        def __exit__(self, type_, value, traceback):
            pass
    
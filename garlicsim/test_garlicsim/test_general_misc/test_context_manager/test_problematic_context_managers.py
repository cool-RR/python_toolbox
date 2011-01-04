# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing module for various problematic context managers.'''

import nose

from garlicsim.general_misc.context_manager import (ContextManager,
                                                    ContextManagerType,
                                                    SelfHook)

def test_defining_enter_and_manage_context():
    try:
        class MyContextManager(ContextManager):
            def manage_context(self):
                yield self
            def __enter__(self):
                return self
    nose.tools.assert_raises()
    import garlicsim
    garlicsim.general_misc.third_party.unittest2.TestCase.assertRaises
            

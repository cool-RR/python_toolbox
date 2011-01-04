# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''This module defines tools for testing.'''

import re

from garlicsim.general_misc import cute_inspect
from garlicsim.general_misc.context_manager import ContextManager
from garlicsim.general_misc import logic_tools


class RaiseAssertor(ContextManager):
    
    def __init__(self, exception_type=Exception, text=''):
        self.exception_type = exception_type
        self.text = text
        self.exception = None
        
    def manage_context(self):
        try:
            yield self
        except self.exception_type, exception:
            self.exception = exception
            if self.text:
                message = exception.args[0]
                if isinstance(self.text, basestring):
                    assert self.text in message
                else:
                    # It's a regex pattern
                    assert self.text.match(message)

                    
def assert_same_signature(*callables):
    arg_specs = [cute_inspect.getargspec(callable_) for callable_ in callables]
    assert logic_tools.all_equal(arg_specs, exhaustive=True)
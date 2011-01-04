# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''This module defines tools for testing.'''

import re

from garlicsim.general_misc.context_manager import ContextManager


class RaiseAssertor(ContextManager):
    
    def __init__(self, exception_type, text):
        self.exception_type = exception_type
        self.text = text
        
    def manage_context(self):
        try:
            yield self
        except self.exception_type as exception:
            if self.text:
                message = exception.args[0]
                if isinstance(self.text, basestring):
                    assert self.text in message
                else:
                    # It's a regex pattern
                    assert self.text.match(message)
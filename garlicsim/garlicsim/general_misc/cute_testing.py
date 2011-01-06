# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''This module defines tools for testing.'''

import re

from garlicsim.general_misc import cute_inspect
from garlicsim.general_misc.context_manager import ContextManager
from garlicsim.general_misc.exceptions import CuteException
from garlicsim.general_misc import logic_tools


class Failure(CuteException):
    '''A test has failed.'''
        

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
                    if self.text not in message:
                        raise Failure("A `%s` was raised but %s wasn't in its "
                                      "message." % (self.exception_type,
                                      repr(self.text)))
                else:
                    # It's a regex pattern
                    if not self.text.match(message):
                        raise Failure("A `%s` was raised but it didn't match "
                                      "the given regex." % self.exception_type)

                    
def assert_same_signature(*callables):
    arg_specs = [cute_inspect.getargspec(callable_) for callable_ in callables]
    if not logic_tools.all_equal(arg_specs, exhaustive=True):
        raise Failure('Not all the callable have the same signature.')
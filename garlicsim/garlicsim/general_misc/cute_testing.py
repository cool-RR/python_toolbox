# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''This module defines tools for testing.'''

import re

from garlicsim.general_misc.third_party import unittest2

from garlicsim.general_misc import cute_inspect
from garlicsim.general_misc.context_manager import ContextManager
from garlicsim.general_misc.exceptions import CuteException
from garlicsim.general_misc import logic_tools


class Failure(CuteException, AssertionError):
    '''A test has failed.'''
        

class RaiseAssertor(ContextManager):
    '''
    Asserts that a certain exception was raised in the suite. You may use a
    snippet of text that must appear in the exception message or a regex that
    the exception message must match.
    
    Example:
    
        with RaiseAssertor(ZeroDivisionError, 'modulo by zero'):
            1/0
    
    '''
    
    def __init__(self, exception_type=Exception, text=''):
        '''
        Construct the `RaiseAssertor`.
        
        `exception_type` is an exception type that the exception must be of;
        `text` may be either a snippet of text that must appear in the
        exception's message, or a regex pattern that the exception message must
        match.
        '''
        self.exception_type = exception_type
        self.text = text
        self.exception = None
        
        
    def manage_context(self):
        '''Manage the `RaiseAssertor'`s context.'''
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
        except BaseException, different_exception:
            raise Failure(
                "%s was excpected, but a different exception %s was raised "
                "instead." % (self.exception_type, type(different_exception))
            )
        else:
            raise Failure("%s wasn't raised." % self.exception_type)

                    
def assert_same_signature(*callables):
    '''Assert that all the `callables` have the same function signature.'''
    arg_specs = [cute_inspect.getargspec(callable_) for callable_ in callables]
    if not logic_tools.all_equal(arg_specs, exhaustive=True):
        raise Failure('Not all the callables have the same signature.')
    
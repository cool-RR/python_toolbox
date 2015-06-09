# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''This module defines tools for testing.'''

import nose
import sys

from python_toolbox.third_party import unittest2

from python_toolbox import cute_inspect
from python_toolbox import context_management
from python_toolbox.exceptions import CuteException
from python_toolbox import logic_tools
from python_toolbox import misc_tools



class Failure(CuteException, AssertionError):
    '''A test has failed.'''


class RaiseAssertor(context_management.ContextManager):
    '''
    Asserts that a certain exception was raised in the suite. You may use a
    snippet of text that must appear in the exception message or a regex that
    the exception message must match.
    
    Example:
    
        with RaiseAssertor(ZeroDivisionError, 'modulo by zero'):
            1/0
    
    '''
    
    def __init__(self, exception_type=Exception, text='',
                 assert_exact_type=False):
        '''
        Construct the `RaiseAssertor`.
        
        `exception_type` is an exception type that the exception must be of;
        `text` may be either a snippet of text that must appear in the
        exception's message, or a regex pattern that the exception message must
        match. Specify `assert_exact_type=False` if you want to assert that the
        exception is of the exact `exception_type` specified, and not a
        subclass of it.
        '''
        self.exception_type = exception_type
        '''The type of exception that should be raised.'''
        
        self.text = text
        '''The snippet or regex that the exception message must match.'''
        
        self.exception = None
        '''The exception that was caught.'''
        
        self.assert_exact_type = assert_exact_type
        '''
        Flag saying whether we require an exact match to `exception_type`.
        
        If set to `False`, a subclass of `exception_type` will also be
        acceptable.
        '''
        
        
    def manage_context(self):
        '''Manage the `RaiseAssertor'`s context.'''
        try:
            yield self
        except self.exception_type as exception:
            self.exception = exception
            if self.assert_exact_type:
                if self.exception_type is not type(exception):
                    assert issubclass(type(exception), self.exception_type)
                    raise Failure(
                        "The exception `%s` was raised, and it *is* an "
                        "instance of the `%s` we were expecting; but its type "
                        "is not `%s`, it's `%s`, which is a subclass of `%s`, "
                        "but you specified `assert_exact_type=True`, so "
                        "subclasses aren't acceptable." % (repr(exception),
                        self.exception_type.__name__,
                        self.exception_type.__name__, type(exception).__name__,
                        self.exception_type.__name__)
                    )
            if self.text:
                message = exception.args[0]
                if isinstance(self.text, str):
                    if self.text not in message:
                        raise Failure(
                            "A `%s` was raised but %s wasn't in its message." %
                            (self.exception_type.__name__, repr(self.text))
                        )
                else:
                    # It's a regex pattern
                    if not self.text.match(message):
                        raise Failure(
                            "A `%s` was raised but it didn't match the given "
                            "regex." % self.exception_type.__name__
                        )
        except BaseException as different_exception:
            raise Failure(
                "%s was excpected, but a different exception %s was raised "
                "instead." % (self.exception_type.__name__,
                              type(different_exception).__name__)
            )
        else:
            raise Failure("%s wasn't raised." % self.exception_type.__name__)

                    
def assert_same_signature(*callables):
    '''Assert that all the `callables` have the same function signature.'''
    arg_specs = [cute_inspect.getargspec(callable_) for callable_ in callables]
    if not logic_tools.all_equivalent(arg_specs, assume_transitive=False):
        raise Failure('Not all the callables have the same signature.')
    
    
class _MissingAttribute:
    '''Object signifying that an attribute was not found.'''
    # todo: make uninstanciable

    
def assert_polite_wrapper(wrapper, wrapped=None, same_signature=True):
    '''
    Assert that `wrapper` is a polite function wrapper around `wrapped`.
    
    A function wrapper (usually created by a decorator) has a few
    responsibilties; maintain the same name, signature, documentation etc. of
    the original function, and a few others. Here we check that the wrapper did
    all of those things.
    '''
    # todo: in all decorators, should be examining the wrapped function's dict
    # and update the new one with it. can't test for this here though, cause
    # the decorator has the right to change them.
    if wrapped is None:
        wrapped = wrapper.__wrapped__
    if same_signature:
        assert_same_signature(wrapper, wrapped)
    for attribute in ('__module__', '__name__', '__doc__', '__annotations__'):
        assert (getattr(wrapper, attribute, None) or _MissingAttribute) == \
               (getattr(wrapped, attribute,  None) or _MissingAttribute)
    assert wrapper.__wrapped__ == wrapped
    
    
class TestCase(unittest2.TestCase, context_management.ContextManager):
    setUp = misc_tools.ProxyProperty('.setup')
    tearDown = misc_tools.ProxyProperty('.tear_down')
    def manage_context(self):
        yield self
        
    def setup(self):
        return self.__enter__()
    def tear_down(self):
        # todo: Should probably do something with exception-swallowing here to
        # abide with the context manager protocol, but I don't need it yet.
        return self.__exit__(*sys.exc_info())
        
        
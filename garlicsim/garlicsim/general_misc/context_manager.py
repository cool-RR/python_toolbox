# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `ContextManager` class.

See its documentation for more information.
'''
# blocktodo: test on pypy

# blocktodo: allow `__enter__` and `__exit__` on different level, just not
# different sides of `manager_context`

# todo: for case of decorated generator, possibly make getstate (or whatever)
# that will cause it to be pickled by reference to the decorated function


from __future__ import with_statement

import types
import sys
from garlicsim.general_misc.third_party import abc

from garlicsim.general_misc.third_party import decorator as decorator_module
from garlicsim.general_misc import monkeypatching_tools


class SelfHook(object):
    # todo: make uninstantiable
    pass


class ContextManagerTypeType(type):
    
    def __call__(cls, *args):
        if len(args) == 1:
            # decorating
            (function,) = args
            assert callable(function)
            name = function.__name__
            bases = (ContextManager,)
            namespace_dict = {}
            context_manager_type = super(ContextManagerTypeType, cls).__call__(
                name,
                bases,
                {'manage_context': staticmethod(function)}
            )
        
            @monkeypatching_tools.monkeypatch_method(context_manager_type)
            def __init__(self, *args, **kwargs):
                self._args, self._kwargs = args, kwargs
                self._ContextManager__generators = []
                
            return context_manager_type
            
        else:
            return super(ContextManagerTypeType, cls).__call__(*args)


class ContextManagerType(abc.ABCMeta):
    
    __metaclass__ = ContextManagerTypeType
    
    def __new__(mcls, name, bases, namespace):
        
        if 'manage_context' in namespace:
            manage_context = namespace['manage_context']
            assert '__enter__' not in namespace
            assert '__exit__' not in namespace
            namespace['__enter__'] = \
                ContextManager._ContextManager__enter_using_manage_context
            namespace['__exit__'] = \
                ContextManager._ContextManager__exit_using_manage_context
        
        return super(ContextManagerType, mcls).__new__(
            mcls,
            name,
            bases,
            namespace
        )
        
    
                    

class ContextManager(object):
    
    
    __metaclass__ = ContextManagerType

    
    def __call__(self, function):
        def inner(function_, *args, **kwargs):
            with self:
                return function_(*args, **kwargs)
        return decorator_module.decorator(inner, function)
    
    
    @abc.abstractmethod
    def __enter__(self):
        pass

    
    @abc.abstractmethod
    def __exit__(self, type_=None, value=None, traceback=None):
        pass
    
    
    def __enter_using_manage_context(self):
        if not hasattr(self, '_ContextManager__generators'):
            self._ContextManager__generators = []
        
        new_generator = self.manage_context(
            *getattr(self, '_args', ()),
            **getattr(self, '_kwargs', {})
        )
        assert isinstance(new_generator, types.GeneratorType)
        self._ContextManager__generators.append(new_generator)
        
        
        try:
            generator_return_value = new_generator.next()
            return self if (generator_return_value is SelfHook) else \
                   generator_return_value
        
        except StopIteration:
            raise RuntimeError("generator didn't yield")
    
        
    def __exit_using_manage_context(self, type_, value, traceback):

        generator = self._ContextManager__generators.pop()
        assert isinstance(generator, types.GeneratorType)
        
        if type_ is None:
            try:
                generator.next()
            except StopIteration:
                return
            else:
                raise RuntimeError("generator didn't stop")
        else:
            if value is None:
                # Need to force instantiation so we can reliably
                # tell if we get the same exception back
                value = type_()
            try:
                generator.throw(type_, value, traceback)
                raise RuntimeError("generator didn't stop after throw()")
            except StopIteration, exc:
                # Suppress the exception *unless* it's the same exception that
                # was passed to throw().  This prevents a StopIteration
                # raised inside the "with" statement from being suppressed
                return exc is not value
            except:
                # only re-raise if it's *not* the exception that was
                # passed to throw(), because __exit__() must not raise
                # an exception unless __exit__() itself failed.  But throw()
                # has to raise the exception to signal propagation, so this
                # fixes the impedance mismatch between the throw() protocol
                # and the __exit__() protocol.
                #
                if sys.exc_info()[1] is not value:
                    raise
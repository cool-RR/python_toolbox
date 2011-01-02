# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `ContextManager` and `ContextManagerType` classes.

These classes allow greater freedom when using context managers; See
`ContextDecorator`'s documentation for more details, or `ContextManagerType`'s
documentation for more details about creating a context manager from a
generator.
'''

# blocktodo: make overriding tests: `manage_context` overriding
# `manage_context`, `manage_context` overriding enter/exit, enter/exit
# overriding enter/exit, enter/exit overriding `manage_context`, enter
# overriding `manage_context` (should raise error) etc.

# blocktodo: allow `__enter__` and `__exit__` on different level, just not
# different sides of `manage_context`

# todo: for case of decorated generator, possibly make getstate (or whatever)
# that will cause it to be pickled by reference to the decorated function


from __future__ import with_statement

import types
import sys
from garlicsim.general_misc.third_party import abc

from garlicsim.general_misc.third_party import decorator as decorator_module


class SelfHook(object):
    '''
    Hook that a context manager can yield in order to yield itself.

    This is useful in context managers which are created from a generator,
    where the user can't do `yield self` because `self` doesn't exist yet.
    
    Example:
    
        @ContextGeneratorType
        def MyContextManager(lock):
            with lock.read:
                yield SelfHook
                
        with MyContextManager(my_lock) as my_context_manager:
            assert isinstance(my_context_manager, MyContextManager)
    
    '''
    # todo: make uninstantiable


class ContextManagerTypeType(type):
    '''Metaclass for `ContextManagerType`. Shouldn't be used directly.'''
    
    def __call__(cls, *args):
        '''
        Create a new `ContextManager`.
        
        This can work in two ways, depending on which arguments are given:
        
         1. The classic `type.__call__` way. If `name, bases, namespace` are
            passed in, `type.__call__` will be used normally.
            
         2. As a decorator for a generator function. For example:
            
                @ContextManagerType
                def MyContextManager():
                    try:
                        yield
                    finally:
                        pass # clean-up
                        
            What happens here is that the function (in this case
            `MyContextManager`) is passed directly into
            `ContextManagerTypeType.__call__`. So we create a new
            `ContextManager` subclass for it, and use the original generator as
            its `.manage_context` function.
                        
        '''
        if len(args) == 1:
            (function,) = args
            assert callable(function)
            name = function.__name__
            bases = (ContextManager,)
            namespace_dict = {
                'manage_context': staticmethod(function),
                '__init__': ContextManager.\
                            _ContextManager__init_lone_manage_context
            }
            return super(ContextManagerTypeType, cls).__call__(
                name,
                bases,
                namespace_dict
            )
            
        else:
            return super(ContextManagerTypeType, cls).__call__(*args)


class ContextManagerType(abc.ABCMeta):
    '''
    Metaclass for `ContextManager`.
    
    Use this directly as a decorator to create a `ContextManager` from a
    generator function.
    
    Example:
    
        @ContextManagerType
        def MyContextManager():
            try:
                yield
            finally:
                pass # clean-up
                
    '''
    
    __metaclass__ = ContextManagerTypeType

    
    def __new__(mcls, name, bases, namespace):
        '''
        Create either `ContextManager` itself or a subclass of it.
        
        If a `manage_context` method is available
        '''
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
    

    def __init_lone_manage_context(self, *args, **kwargs):
        self._ContextManager__args = args
        self._ContextManager__kwargs = kwargs
        self._ContextManager__generators = []
    
    
    def __enter_using_manage_context(self):
        if not hasattr(self, '_ContextManager__generators'):
            self._ContextManager__generators = []
        
        new_generator = self.manage_context(
            *getattr(self, '_ContextManager__args', ()),
            **getattr(self, '_ContextManager__kwargs', {})
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
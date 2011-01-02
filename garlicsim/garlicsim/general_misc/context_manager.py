# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `ContextManager` and `ContextManagerType` classes.

These classes allow for greater freedom both when (a) defining context managers
and when (b) using them.

Inherit all your context managers from `ContextManager` (or decorate your
generator functions with `ContextManagerType`) to enjoy all the benefits
described below.


Defining context managers
-------------------------

There are 3 different ways in which context managers can be defined, and each
has their own advantages and disadvantages over the others.

 1. The classic way to define a context manager is to define a class with 
    `__enter__` and `__exit__` methods. This is allowed, and if you do this
    you should still inherit from `ContextManager`. Example:
     
        class MyContextManager(ContextManager):
            def __enter__(self):
                pass # preparation
            def __exit__(self, type_=None, value=None, traceback=None):
                pass # cleanup
     
 2. As a decorated generator, like so:
    
        @ContextManagerType
        def MyContextManager():
            try:
                yield
            finally:
                pass # clean-up
                
    This usage is nothing new; It's also available when using the standard
    library's `contextlib.contextmanager` decorator. One thing that is allowed
    here that `contextlib` doesn't allow is to yield the context manager itself
    by doing `yield SelfHook`.
    
 3. The third and novel way is by defining a class with a `manage_context`
    method which returns a decorator. Example:
    
        class MyContextManager(ContextManager):
            def manage_context(self):
                do_some_prepartion()
                try:
                    with some_lock:
                        yield self
                finally:
                    do_some_cleanup()
                    
    This approach is sometimes cleaner than defining `__enter__` and
    `__exit__`; Especially when using another context manager inside
    `manage_context`. In our example we did `with some_lock` in our
    `manage_context`, which is shorter and more idiomatic than calling
    `some_lock.__enter__` in an `__enter__` method and `some_lock.__exit__` in
    an `__exit__` method.
    
    
These were the different ways of *defining* a context manager. Now let's see
the different ways of *using* a context manager:


Using context managers
----------------------

There are 2 different ways in which context managers can be used:

 1. The plain old honest-to-Guido `with` keyword:
 
       with MyContextManager() as my_context_manager:
           do_stuff()
           
 2. As a decorator to a function
 
        @MyContextManager()
        def do_stuff():
           pass # doing stuff
           
    When the `do_stuff` function will be called, the context manager will be
    used. This functionality is also available in the standard library of
    Python 3.2+ by using `contextlib.ContextDecorator`, but here it is combined
    with all the other goodies given by `ContextManager`.

    
That's it. Inherit all your context managers from `ContextManager` (or decorate
your generator functions with `ContextManagerType`) to enjoy all these
benefits.
'''

# blocktodo: make tests: `__enter__` overriding `manage_context` (should raise error)
# etc.

# blocktodo: allow `__enter__` and `__exit__` on different level, just not
# different sides of `manage_context`. make tests.

# blocktodo: test signature perservation

# todo: test using as abc with other abstract functions

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
                
    The resulting context manager could be called either with the `with`
    keyword or by using it as a decorator to a function.
                
    For more details, see documentation of the containing module,
    `garlicsim.general_misc.context_manager`.
    '''
    
    __metaclass__ = ContextManagerTypeType

    
    def __new__(mcls, name, bases, namespace):
        '''
        Create either `ContextManager` itself or a subclass of it.
        
        For subclasses of `ContextManager`, if a `manage_context` method is
        available, we will use `__enter__` and `__exit__` that will use the
        generator returned by `manage_context`.
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
    '''
    Allows running preperation code before a given suite and cleanup after.
    
    To make a context manager, use `ContextManager` as a base class and either
    (a) define `__enter__` and `__exit__` methods or (b) define a
    `manage_context` method that returns a generator. An alternative way to
    create a context manager is to define a generator function and decorate it
    with `ContextManagerType`.
    
    In any case, the resulting context manager could be called either with the
    `with` keyword or by using it as a decorator to a function.
                
    For more details, see documentation of the containing module,
    `garlicsim.general_misc.context_manager`.
    '''
    
    
    __metaclass__ = ContextManagerType

    
    def __call__(self, function):
        '''Decorate `function` to use this context manager when it's called.'''
        def inner(function_, *args, **kwargs):
            with self:
                return function_(*args, **kwargs)
        return decorator_module.decorator(inner, function)
    
    
    @abc.abstractmethod
    def __enter__(self):
        '''Prepare for suite execution.'''

    
    @abc.abstractmethod
    def __exit__(self, type_=None, value=None, traceback=None):
        '''Cleanup after suite execution.'''
    

    def __init_lone_manage_context(self, *args, **kwargs):
        '''
        Initialize a `ContextManager` made from a lone generator function.
        '''
        self._ContextManager__args = args
        self._ContextManager__kwargs = kwargs
        self._ContextManager__generators = []
    
    
    def __enter_using_manage_context(self):
        '''
        Prepare for suite execution.
        
        This is used as `__enter__` for context managers that use a
        `manage_context` function.
        '''
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
        '''
        Cleanup after suite execution.
        
        This is used as `__exit__` for context managers that use a
        `manage_context` function.
        '''
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
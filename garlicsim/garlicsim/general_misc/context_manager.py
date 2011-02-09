# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `ContextManager` and `ContextManagerType` classes.

Using these classes to define context managers allows using such context
managers as decorators (in addition to their normal use) and supports writing
context managers in a new form called `manage_context`. (As well as the
original forms).

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
            # preparation
            try:
                yield
            finally:
                pass # cleanup
                
    The advantage of this approach is its brevity, and it may be a good fit for
    relatively simple context managers that don't require defining an actual
    class.
                
    This usage is nothing new; It's also available when using the standard
    library's `contextlib.contextmanager` decorator. One thing that is allowed
    here that `contextlib` doesn't allow is to yield the context manager itself
    by doing `yield SelfHook`.
    
 3. The third and novel way is by defining a class with a `manage_context`
    method which returns a decorator. Example:
    
        class MyContextManager(ContextManager):
            def manage_context(self):
                do_some_preparation()
                with other_context_manager:
                    yield self
                    
    This approach is sometimes cleaner than defining `__enter__` and
    `__exit__`; especially when using another context manager inside
    `manage_context`. In our example we did `with other_context_manager` in our
    `manage_context`, which is shorter, more idiomatic and less
    double-underscore-y than the equivalent classic definition:

        class MyContextManager(object):
                def __enter__(self):
                    do_some_preparation()
                    other_context_manager.__enter__()
                    return self
                def __exit__(self, *exc):
                    return other_context_manager.__exit__(*exc)
    
    Another advantage of this approach over `__enter__` and `__exit__` is that
    it's better at handling exceptions, since any exceptions would be raised
    inside `manage_context` where we could `except` them, which is much more
    idiomatic than the way `__exit__` handles exceptions, which is by receiving
    their type and returning whether to swallow them or not.
    
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

# todo: review the few external tests that I'm skipping.

# todo: test using as abc with other abstract functions

# todo: can make a helpful exception message for when the user decorates with
# `ContextManager` instead of `ContextManagerType`

# todo: for case of decorated generator, possibly make getstate (or whatever)
# that will cause it to be pickled by reference to the decorated function


from __future__ import with_statement

import types
import sys
from garlicsim.general_misc.third_party import abc

from garlicsim.general_misc import decorator_tools


class SelfHook(object):
    '''
    Hook that a context manager can yield in order to yield itself.

    This is useful in context managers which are created from a generator
    function, where the user can't do `yield self` because `self` doesn't exist
    yet.
    
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
                    # preparation
                    try:
                        yield
                    finally:
                        pass # cleanup
                        
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
            # preparation
            try:
                yield
            finally:
                pass # cleanup
                
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
            if '__enter__' in namespace:
                raise Exception(
                    'You defined both an `__enter__` method and a '
                    '`manage_context` method-- That is unallowed. You need to '
                    '*either* define a `manage_context` method *or* an '
                    '`__enter__` and `__exit__` pair.'
                )
            if '__exit__' in namespace:
                raise Exception(
                    'You defined both an `__exit__` method and a '
                    '`manage_context` method-- That is unallowed. You need to '
                    '*either* define a `manage_context` method *or* an '
                    '`__enter__` and `__exit__` pair.'
                )
            namespace['__enter__'] = \
                ContextManager._ContextManager__enter_using_manage_context
            namespace['__exit__'] = \
                ContextManager._ContextManager__exit_using_manage_context
            
        result_class = super(ContextManagerType, mcls).__new__(
            mcls,
            name,
            bases,
            namespace
        )
        
        
        if (not result_class.__is_the_base_context_manager_class()) and \
           ('manage_context' not in namespace) and \
           hasattr(result_class, 'manage_context'):
            
            # What this `if` just checked for is: Is this a class that doesn't
            # define `manage_context`, but whose base context manager class
            # *does* define `manage_context`?
            #
            # If so, we need to be careful. It's okay for this class to be
            # using the enter/exit pair provided by the base `manage_context`;
            # It's also okay for this class to override these with its own
            # `__enter__` and `__exit__` implementations; But it's *not* okay
            # for this class to define just one of these methods, say
            # `__enter__`, because then it will not have an `__exit__` to work
            # with.
            
            our_enter_uses_manage_context = (
                getattr(result_class.__enter__, 'im_func',
                result_class.__enter__) == ContextManager.\
                _ContextManager__enter_using_manage_context.im_func
            )
            
            our_exit_uses_manage_context = (
                getattr(result_class.__exit__, 'im_func',
                result_class.__exit__) == ContextManager.\
                _ContextManager__exit_using_manage_context.im_func
            )
            
            if our_exit_uses_manage_context and not \
               our_enter_uses_manage_context:
                
                assert '__enter__' in namespace
            
                raise Exception("The %s class defines an `__enter__` method, "
                                "but not an `__exit__` method; We cannot use "
                                "the `__exit__` method of its base context "
                                "manager class because it uses the "
                                "`manage_context` generator function." %
                                result_class)

            
            if our_enter_uses_manage_context and not \
               our_exit_uses_manage_context:
                
                assert '__exit__' in namespace
                
                raise Exception("The %s class defines an `__exit__` method, "
                                "but not an `__enter__` method; We cannot use "
                                "the `__enter__` method of its base context "
                                "manager class because it uses the "
                                "`manage_context` generator function." %
                                result_class)
            
        return result_class

    
    def __is_the_base_context_manager_class(cls):
        '''
        Return whether `cls` is `ContextManager`.
        
        It's an ugly method, but unfortunately it's necessary because at one
        point we want to test if a class is `ContextManager` before
        `ContextManager` is defined in this module.
        '''
        
        return (
            (cls.__name__ == 'ContextManager') and
            (cls.__module__ == 'garlicsim.general_misc.context_manager') and
            (cls.mro() == [cls, object])
        )
                
    
class ContextManager(object):
    '''
    Allows running preparation code before a given suite and cleanup after.
    
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
        return decorator_tools.decorator(inner, function)
    
    
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
            raise RuntimeError("The generator didn't yield even one time; It "
                               "must yield one time exactly.")
    
        
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
                raise RuntimeError(
                    "The generator didn't stop after the yield; Possibly you "
                    "have more than one `yield` in the generator function? "
                    "The generator function must yield exactly one time.")
        else:
            if value is None:
                # Need to force instantiation so we can reliably
                # tell if we get the same exception back
                value = type_()
            try:
                generator.throw(type_, value, traceback)
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
            else:
                raise RuntimeError(
                    "The generator didn't stop after calling its `.throw()`; "
                    "Possibly you have more than one `yield` in the generator "
                    "function? The generator function must yield exactly one "
                    "time."
                )
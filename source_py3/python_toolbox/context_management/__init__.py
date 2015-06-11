# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

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
            def __exit__(self, exc_type, exc_value, exc_traceback):
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
                
    This usage is nothing new; it's also available when using the standard
    library's `contextlib.contextmanager` decorator. One thing that is allowed
    here that `contextlib` doesn't allow is to yield the context manager itself
    by doing `yield SelfHook`.
    
 3. The third and novel way is by defining a class with a `manage_context`
    method which returns a generator. Example:
    
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

        class MyContextManager:
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


This package also defines a bunch of helpful context manager classes on top of
`ContextManager`: Those are `BlankContextManager`, `ReentrantContextManager`
and `DelegatingContextManager`. See these classes' docstrings for more info.
'''

# todo: review the few external tests that I'm skipping.

# todo: test using as abc with other abstract functions

# todo: can make a helpful exception message for when the user decorates with
# `ContextManager` instead of `ContextManagerType`

# todo: for case of decorated generator, possibly make getstate (or whatever)
# that will cause it to be pickled by reference to the decorated function


from .context_manager_type_type import ContextManagerTypeType
from .context_manager_type import ContextManagerType
from .context_manager import ContextManager
from .self_hook import SelfHook

from .blank_context_manager import BlankContextManager
from .reentrant_context_manager import ReentrantContextManager
from .delegating_context_manager import DelegatingContextManager
from .functions import nested
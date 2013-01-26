# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''Tools for monkeypatching.'''

import types

from python_toolbox import decorator_tools
from python_toolbox import caching


@decorator_tools.helpful_decorator_builder
def monkeypatch_method(class_, name=None):
    '''
    Monkeypatch a method into a class.
    
    Example:
    
        class A(object):
            pass
    
        @monkeypatch_method(A)
        def my_method(a):
            return (a, 'woo!')
        
        a = A()
        
        assert a.my_method() == (a, 'woo!')
        
    You may use the `name` argument to specify a method name different from the
    function's name.
    
    You can also use this to monkeypatch a `CachedProperty` into a class.
    '''
    def decorator(function):
        # Note that unlike most decorators, this decorator retuns the function
        # it was given without modifying it. It modifies the class only.
        if isinstance(function, types.FunctionType):
            name_ = name or function.__name__
            new_method = types.MethodType(function, None, class_)
            # todo: Last line was: `new_method = types.MethodType(function,
            # class_)`, is subtly wrong, make tests to prove
            setattr(class_, name_, new_method)
            return function
        else:
            assert isinstance(function, caching.CachedProperty)
            cached_property = function
            if not isinstance(cached_property.getter, types.FunctionType):
                raise NotImplemented
            name_ = cached_property.getter.__name__
            setattr(class_, name_, cached_property)
            return cached_property
    return decorator
# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''Tools for monkeypatching.'''

import sys
import types

from python_toolbox import misc_tools
from python_toolbox import decorator_tools
from python_toolbox import caching


@decorator_tools.helpful_decorator_builder
def monkeypatch_method(monkeypatchee, name=None):
    '''
    Monkeypatch a method into a class (or an object).
    
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
    
    You can also use this to monkeypatch a `CachedProperty`, a `classmethod`
    and a `staticmethod` into a class.
    '''
    
    monkeypatchee_is_a_class = misc_tools.is_type(monkeypatchee)
    class_of_monkeypatchee = monkeypatchee if monkeypatchee_is_a_class else \
                                      misc_tools.get_actual_type(monkeypatchee)
    
    def decorator(function):
        # Note that unlike most decorators, this decorator retuns the function
        # it was given without modifying it. It modifies the class only.
        if isinstance(function, types.FunctionType):
            name_ = name or function.__name__
            
            new_method = types.MethodType(function, None, monkeypatchee) if \
                monkeypatchee_is_a_class else types.MethodType(function,
                                         monkeypatchee, class_of_monkeypatchee)
            setattr(monkeypatchee, name_, new_method)
            return function
        else:
            # `function` is probably some kind of descriptor.
            if not monkeypatchee_is_a_class:
                raise NotImplementedError(
                    "I don't know how to monkeypatch a descriptor onto a "
                    "non-class object."
                )
            if not name:
                ### Getting name of descriptor: ###############################
                #                                                             #
                if isinstance(function, caching.CachedProperty):
                    if not isinstance(function.getter, types.FunctionType):
                        raise NotImplemented
                    name_ = function.getter.__name__
                elif isinstance(function, (classmethod, staticmethod)):
                    name_ = function.__func__.__name__
                elif isinstance(function, property):
                    name_ = function.fget.__name__
                else:
                    raise NotImplementedError(
                        "`monkeypatch_method` doesn't know how to get the "
                        "name of this kind of function automatically, try "
                        "manually."
                    )
                #                                                             #
                ### Finished getting name of descriptor. ######################
            setattr(monkeypatchee, name_, function)
            return function
        
    return decorator


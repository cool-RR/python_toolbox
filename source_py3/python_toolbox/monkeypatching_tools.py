# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Tools for monkeypatching.'''

import collections
import inspect
import types

from python_toolbox import misc_tools
from python_toolbox import dict_tools
from python_toolbox import decorator_tools
from python_toolbox import caching


@decorator_tools.helpful_decorator_builder
def monkeypatch(monkeypatchee, name=None, override_if_exists=True):
    '''
    Monkeypatch a method into a class (or object), or any object into module.
    
    Example:
    
        class A:
            pass
    
        @monkeypatch(A)
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
                                                            type(monkeypatchee)
    
    def decorator(function):
        # Note that unlike most decorators, this decorator retuns the function
        # it was given without modifying it. It modifies the class/module only.
        if isinstance(monkeypatchee, types.ModuleType):
            name_ = name or function.__name__
            setattr_value = return_value = function
        elif isinstance(function, types.FunctionType):
            name_ = name or function.__name__
            
            new_method = function if monkeypatchee_is_a_class else \
                             types.MethodType(function, class_of_monkeypatchee)
            setattr_value = new_method
            return_value = function
        else:
            # `function` is probably some kind of descriptor.
            if not monkeypatchee_is_a_class:
                raise NotImplementedError(
                    "I don't know how to monkeypatch a descriptor onto a "
                    "non-class object."
                )
            if name:
                name_ = name
            else:
                ### Getting name of descriptor: ###############################
                #                                                             #
                if isinstance(function, caching.CachedProperty):
                    if not isinstance(function.getter, types.FunctionType):
                        raise NotImplementedError
                    name_ = function.getter.__name__
                elif isinstance(function, (classmethod, staticmethod)):
                    name_ = function.__func__.__name__
                elif isinstance(function, property):
                    name_ = function.fget.__name__
                else:
                    raise NotImplementedError(
                        "`monkeypatch` doesn't know how to get the "
                        "name of this kind of function automatically, try "
                        "manually."
                    )
                #                                                             #
                ### Finished getting name of descriptor. ######################
            setattr_value = return_value = function

        if override_if_exists or not hasattr(monkeypatchee, name_):
            setattr(monkeypatchee, name_, setattr_value)
        return return_value
        
    return decorator


def change_defaults(function=None, new_defaults={}):
    '''
    Change default values of a function.
    
    Include the new defaults in a dict `new_defaults`, with each key being a
    keyword name and each value being the new default value.
    
    Note: This changes the actual function!
    
    Can be used both as a straight function and as a decorater to a function to
    be changed.
    '''
    def change_defaults_(function_, new_defaults_):
        signature = inspect.Signature.from_function(function_)
        defaults = list(function_.__defaults__ or ())
        kwdefaults = function_.__kwdefaults__ or {}
        defaultful_parameters = dict_tools.filter_items(
            signature.parameters,
            lambda name, parameter: parameter.default != inspect._empty,
            force_dict_type=collections.OrderedDict
        )
        (keyword_only_defaultful_parameters,
         non_keyword_only_defaultful_parameters) = dict_tools.filter_items(
             defaultful_parameters,
             lambda name, parameter: parameter.kind == inspect._KEYWORD_ONLY,
             double=True, 
         )
        
        non_existing_arguments = set(new_defaults) - set(defaultful_parameters)
        if non_existing_arguments:
            raise Exception("Arguments %s are not defined, or do not have a "
                            "default defined. (Can't create default value for "
                            "argument that has no existing default.)"
                            % non_existing_arguments)
        
        for parameter_name in keyword_only_defaultful_parameters:
            if parameter_name in new_defaults_:
                kwdefaults[parameter_name] = new_defaults_[parameter_name]
                
        for i, parameter_name in \
                             enumerate(non_keyword_only_defaultful_parameters):
            if parameter_name in new_defaults_:
                defaults[i] = new_defaults_[parameter_name]
                
        function_.__defaults__ = tuple(defaults)
        function_.__kwdefaults__ = kwdefaults
        
        return function_

    if not callable(function):
        # Decorator mode:
        if function is None:
            actual_new_defaults = new_defaults
        else:
            actual_new_defaults = function
        return lambda function_: change_defaults_(function_,
                                                  actual_new_defaults)
    else:
        # Normal usage mode:
        return change_defaults_(function, new_defaults)
        
        
    
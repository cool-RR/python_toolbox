# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''
Defines the `CachedType` metaclass.

See its documentation for more details.
'''

from python_toolbox.sleek_reffing import SleekCallArgs


class SelfPlaceholder(object):
    '''Placeholder for `self` when storing call-args.''' 


class CachedType(type):
    '''
    A metaclass for sharing instances.
        
    For example, if you have a class like this:
    
        class Grokker(object):
            
            __metaclass__ = caching.CachedType
            
            def __init__(self, a, b=2):
                self.a = a
                self.b = b
                
    Then all the following calls would result in just one instance:
    
        Grokker(1) is Grokker(1, 2) is Grokker(b=2, a=1) is Grokker(1, **{})
    
    This metaclass understands keyword arguments.
    
    All the arguments are sleekreffed to prevent memory leaks. Sleekref is a
    variation of weakref. Sleekref is when you try to weakref an object, but if
    it's non-weakreffable, like a `list` or a `dict`, you maintain a normal,
    strong reference to it. (See documentation of
    `python_toolbox.sleek_reffing` for more details.) Thanks to sleekreffing
    you can avoid memory leaks when using weakreffable arguments, but if you
    ever want to use non-weakreffable arguments you are still able to.
    (Assuming you don't mind the memory leaks.)
    '''
    
    def __new__(mcls, *args, **kwargs):
        result = super(CachedType, mcls).__new__(mcls, *args, **kwargs)
        result.__cache = {}
        return result

    
    def __call__(cls, *args, **kwargs):
        sleek_call_args = SleekCallArgs(
            cls.__cache,
            cls.__init__,
            *((SelfPlaceholder,) + args),
            **kwargs
        )
        try:
            return cls.__cache[sleek_call_args]
        except KeyError:
            cls.__cache[sleek_call_args] = value = \
                super(CachedType, cls).__call__(*args, **kwargs)
            return value

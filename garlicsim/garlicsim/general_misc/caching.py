
# tododoc: Must use weakref, otherwise all garbage-collection goes kaput!

import functools
import weakref

from garlicsim.general_misc.arguments_profile import ArgumentsProfile
from garlicsim.general_misc.sleek_refs import (SleekRef,
                                               CuteSleekValueDictionary,
                                               SleekCallArgs)


def cache(function):
    
    # In case we're being given a function that is already cached:
    if hasattr(function, 'cache'): return function
    
    cache_dict = {}
    
    def cached(*args, **kwargs):
        sleek_call_args = SleekCallArgs(cache_dict, function, *args, **kwargs)
        try:
            return cached.cache[sleek_call_args]
        except KeyError:
            cached.cache[sleek_call_args] = value = function(*args, **kwargs)
            return value
            
    cached.cache = cache_dict
    
    functools.update_wrapper(cached, function)
    
    return cached

class SelfPlaceholder(object):
    pass # todo: make uninstanciable

class CachedType(type):
    def __new__(self, *args, **kwargs):
        result = type.__new__(self, *args, **kwargs)
        result.__cache = {}
        return result
    
    def __call__(cls, *args, **kwargs):
        # todo: should not use the generic cache function. need to analyze
        # signature of __init__. Possibly use the same args&kwargs grokker for
        # this and `cache`.
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
                type.__call__(cls, *args, **kwargs)
            return value
    

class LazilyEvaluatedConstantProperty(object):
    '''
    A property that is calculated (a) lazily and (b) only once for an object.
    
    Usage:
    
        class MyObject(object):
        
            # ... Regular definitions here
        
            def _get_personality(self):
                print('Calculating personality...')
                time.sleep(5) # Time consuming process that creates personality
                return 'Nice person'
        
            personality = LazilyEvaluatedConstantProperty(_get_personality)
    
    '''
    def __init__(self, getter, name=None):
        '''
        Construct the LEC-property.
        
        You may optionally pass in the name the this property has in the class;
        This will save a bit of processing later.
        '''
        self.getter = getter
        self.our_name = name
        
        
    def __get__(self, obj, our_type=None):

        if not obj:
            # We're being accessed from the class itself, not from an object
            return self
        
        value = self.getter(obj)
        
        if not self.our_name:
            if not our_type:
                our_type = type(obj)
            (self.our_name,) = (key for (key, value) in 
                                vars(our_type).iteritems()
                                if value is self)
        
        setattr(obj, self.our_name, value)
        
        return value

    
        
    
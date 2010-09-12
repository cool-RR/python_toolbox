
# tododoc: Must use weakref, otherwise all garbage-collection goes kaput!

import functools
import weakref
from garlicsim.general_misc.third_party import inspect

from garlicsim.general_misc.arguments_profile import ArgumentsProfile
from garlicsim.general_misc.sleek_ref import SleekRef
from garlicsim.general_misc.weakref_tools import CuteWeakValueDictionary


class SleekCallArgs(object):
    def __init__(self, containing_dict, function, *args, **kwargs):
        
        self.containing_dict = containing_dict
        
        args_spec = inspect.getargspec(function)
        star_args_name, star_kwargs_name = \
                      args_spec.varargs, args_spec.keywords
        
        call_args = inspect.getcallargs(function, *args, **kwargs)
        del args, kwargs
        
        self.weak_key_dict = weakref.WeakKeyDictionary()
        
        star_args = call_args.pop(star_args_name, None)
        self.star_args_refs = [
            SleekRef(star_arg, self.destroy) for star_arg in star_args
        ]
        
        star_kwargs = call_args.pop(star_kwargs_name, None)
        self.star_kwargs_refs = CuteWeakValueDictionary(
            self.destroy,
            star_kwargs
        )
        
        self.args_refs = CuteWeakValueDictionary(
            self.destroy,
            call_args
        )
    
    args = property(lambda self: dict(self.args_refs))
    
    star_args = property(
        lambda self:
            tuple((star_arg_ref() for star_arg_ref in self.star_arg_refs))
    )
    
    star_kwargs = property(lambda self: dict(self.star_kwargs_refs))
    
        
    def destroy(self, _=None):
        try:
            del self.containing_dict[self]
        except KeyError:
            pass
        
    def __hash__(self):
        return hash(
            (
                self.args,
                self.star_args,
                self.star_kwargs
            )
        )
        
        

#class SleekCallArgsDict(dict):
    #def __init__(self, *args, **kwargs):
        #dict.__init__(self, *args, **kwargs)
        

def cache(function):
    # todo: kwargs support
    # todo: try to be smart and figure out the function's signature, then be
    # able to understand that squared(x) is the same as sqaured(number=x).
    
    # In case we're being given a function that is already cached:
    if hasattr(function, 'cache'): return function
    
    def cached(*args, **kwargs):
        callargs = inspect.getcallargs(function, *args, **kwargs)
        try:
            return cached.cache[arguments_profile]
        except KeyError:
            cached.cache[arguments_profile] = value = \
                  function(*arguments_profile.args,
                           **arguments_profile.kwargs)
            return value
            
    cached.cache = {} # weakref.WeakKeyDictionary()
    # todo: no weakref on this baby, be advised
    
    functools.update_wrapper(cached, function)
    
    return cached


class CachedType(type):
    @cache
    def __call__(cls, *args, **kwargs):
        # todo: should not use the generic cache function. need to analyze
        # signature of __init__. Possibly use the same args&kwargs grokker for
        # this and `cache`.
        return type.__call__(cls, *args, **kwargs)
    

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

    
        
    
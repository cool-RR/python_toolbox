
# tododoc: Must use weakref, otherwise all garbage-collection goes kaput!

import functools
import weakref

from garlicsim.general_misc.sleek_refs import SleekCallArgs



def cache(function):
    # todo idea: figure how how complex the function's argspec is, and then
    # compile a function accordingly, so functions with a simple argspec won't
    # have to go through so much shit.
    
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

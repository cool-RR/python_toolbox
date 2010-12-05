
import functools
import weakref

from garlicsim.general_misc.sleek_refs import SleekCallArgs
from garlicsim.general_misc.infinity import Infinity
from garlicsim.general_misc.third_party.ordered_dict import OrderedDict



def cache(max_size=Infinity):
    # todo idea: figure how how complex the function's argspec is, and then
    # compile a function accordingly, so functions with a simple argspec won't
    # have to go through so much shit. update: probably it will help only for
    # completely argumentless function. so do one for those.
    
    # todo: if user put a function instead of `max_size`, give helpful exception
    # message.

    if max_size == Infinity:
        
        def decorator(function):
            # In case we're being given a function that is already cached:
            if hasattr(function, 'cache'): return function
            
            cache_dict = {}
            
            def cached(*args, **kwargs):
                sleek_call_args = \
                    SleekCallArgs(cache_dict, function, *args, **kwargs)
                try:
                    return cached.cache[sleek_call_args]
                except KeyError:
                    cached.cache[sleek_call_args] = value = \
                          function(*args, **kwargs)
                    return value
                    
            cached.cache = cache_dict
            
            functools.update_wrapper(cached, function)
            
            return cached
        
    else: # max_size < Infinity
        
        def decorator(function):
            # In case we're being given a function that is already cached:
            if hasattr(function, 'cache'): return function
            
            cache_dict = OrderedDict()
            
            def cached(*args, **kwargs):
                sleek_call_args = \
                    SleekCallArgs(cache_dict, function, *args, **kwargs)
                try:
                    return cached.cache[sleek_call_args]
                except KeyError:
                    cached.cache[sleek_call_args] = value = \
                        function(*args, **kwargs)
                    if len(cached.cache) > max_size:
                        cached.cache.popitem(last=False)
                    return value
                    
            cached.cache = cache_dict
            
            functools.update_wrapper(cached, function)
            
            return cached
        
    return decorator

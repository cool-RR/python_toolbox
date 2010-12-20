# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `cache` decorator.

See its documentation for more details.
'''

import functools

from garlicsim.general_misc.sleek_refs import SleekCallArgs
from garlicsim.general_misc.infinity import infinity
from garlicsim.general_misc import misc_tools
from garlicsim.general_misc.third_party.ordered_dict import OrderedDict



def cache(max_size=infinity):
    # todo idea: figure how how complex the function's argspec is, and then
    # compile a function accordingly, so functions with a simple argspec won't
    # have to go through so much shit. update: probably it will help only for
    # completely argumentless function. so do one for those.
    
    if callable(max_size) and not misc_tools.is_number(max_size):
        raise TypeError('You entered the callable `%s` where you should have '
                        'entered the `max_size` for the cache. You probably '
                        'used `@cache`, while you should have used `@cache()`')

    if max_size == infinity:
        
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
        
    else: # max_size < infinity
        
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

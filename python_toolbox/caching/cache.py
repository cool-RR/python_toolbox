# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `cache` decorator.

See its documentation for more details.
'''
# todo: examine thread-safety

import functools

from garlicsim.general_misc import decorator_tools

from garlicsim.general_misc.sleek_refs import SleekCallArgs
from garlicsim.general_misc.infinity import infinity
from garlicsim.general_misc.nifty_collections import OrderedDict


@decorator_tools.helpful_decorator_builder
def cache(max_size=infinity):
    '''
    Cache a function, saving results so they won't have to be computed again.
    
    This decorator understands function arguments. For example, it understands
    that for a function like this:

        @cache()
        def f(a, b=2):
            return whatever
            
    The calls `f(1)` or `f(1, 2)` or `f(b=2, a=1)` are all identical, and a
    cached result saved for one of these calls will be used for the others.
    
    All the arguments are sleekreffed to prevent memory leaks. Sleekref is a
    variation of weakref. Sleekref is when you try to weakref an object, but if
    it's non-weakreffable, like a `list` or a `dict`, you maintain a normal,
    strong reference to it. (See documentation of
    `garlicsim.general_misc.sleek_refs` for more details.) Thanks to
    sleekreffing you can avoid memory leaks when using weakreffable arguments,
    but if you ever want to use non-weakreffable arguments you are still able
    to. (Assuming you don't mind the memory leaks.)
    
    You may optionally specify a `max_size` for maximum number of cached
    results to store; old entries are thrown away according to a
    least-recently-used alogrithm. (Often abbreivated LRU.)
    '''
    # todo idea: figure how how complex the function's argspec is, and then
    # compile a function accordingly, so functions with a simple argspec won't
    # have to go through so much shit. update: probably it will help only for
    # completely argumentless function. so do one for those.

    def decorator(function):
        
        # In case we're being given a function that is already cached:
        if getattr(function, 'is_cached', False): return function
        
        if max_size == infinity:
            
            cache_dict = {}

            def cached(function, *args, **kwargs):
                sleek_call_args = \
                    SleekCallArgs(cache_dict, function, *args, **kwargs)
                try:
                    return cached._cache[sleek_call_args]
                except KeyError:
                    cached._cache[sleek_call_args] = value = \
                          function(*args, **kwargs)
                    return value
    
        else: # max_size < infinity
            
            cache_dict = OrderedDict()
            
            def cached(function, *args, **kwargs):
                sleek_call_args = \
                    SleekCallArgs(cache_dict, function, *args, **kwargs)
                try:
                    result = cached._cache[sleek_call_args]
                    cached._cache.move_to_end(sleek_call_args)
                    return result
                except KeyError:
                    cached._cache[sleek_call_args] = value = \
                        function(*args, **kwargs)
                    if len(cached._cache) > max_size:
                        cached._cache.popitem(last=False)
                    return value
                    
        cached._cache = cache_dict
        
        result = decorator_tools.decorator(cached, function)
        
        def cache_clear():
            '''Clear the cache, deleting all saved results.'''
            cached._cache.clear()    
        result.cache_clear = cache_clear
        
        result.is_cached = True
        
        return result
        
    return decorator

# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''
Defines the `cache` decorator.

See its documentation for more details.
'''
# todo: examine thread-safety

import datetime as datetime_module

from python_toolbox import misc_tools
from python_toolbox import binary_search
from python_toolbox import decorator_tools
from python_toolbox.sleek_reffing import SleekCallArgs

infinity = float('inf')


class CLEAR_ENTIRE_CACHE(misc_tools.NonInstantiable):
    '''Sentinel object for clearing the entire cache.'''


def _get_now():
    '''
    Get the current datetime.
    
    This is specified as a function to make testing easier.
    '''
    return datetime_module.datetime.now()


@decorator_tools.helpful_decorator_builder
def cache(max_size=infinity, time_to_keep=None):
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
    `python_toolbox.sleek_reffing` for more details.) Thanks to sleekreffing
    you can avoid memory leaks when using weakreffable arguments, but if you
    ever want to use non-weakreffable arguments you are still able to.
    (Assuming you don't mind the memory leaks.)
    
    You may optionally specify a `max_size` for maximum number of cached
    results to store; old entries are thrown away according to a
    least-recently-used alogrithm. (Often abbreivated LRU.)
    
    You may optionally specific a `time_to_keep`, which is a time period after
    which a cache entry will expire. (Pass in either a `timedelta` object or
    keyword arguments to create one.)
    '''
    # todo idea: figure how how complex the function's argspec is, and then
    # compile a function accordingly, so functions with a simple argspec won't
    # have to go through so much shit. update: probably it will help only for
    # completely argumentless function. so do one for those.
    
    from python_toolbox.nifty_collections import OrderedDict
    
    if time_to_keep is not None:
        if max_size != infinity:
            raise NotImplementedError
        if not isinstance(time_to_keep, datetime_module.timedelta):
            try:
                time_to_keep = datetime_module.timedelta(**time_to_keep)
            except Exception:
                raise TypeError(
                    '`time_limit` must be either a `timedelta` object or a '
                    'dict of keyword arguments for constructing a '
                    '`timedelta` object.'
                )
        assert isinstance(time_to_keep, datetime_module.timedelta)
        

    def decorator(function):
        
        # In case we're being given a function that is already cached:
        if getattr(function, 'is_cached', False): return function
        
        if max_size == infinity:
            
            if time_to_keep:

                sorting_key_function = lambda sleek_call_args: \
                                              cached._cache[sleek_call_args][1]

                
                def remove_expired_entries():
                    almost_cutting_point = \
                                          binary_search.binary_search_by_index(
                        list(cached._cache.keys()),
                        _get_now(), 
                        sorting_key_function,
                        rounding=binary_search.LOW
                    )
                    if almost_cutting_point is not None:
                        cutting_point = almost_cutting_point + 1
                        for key in cached._cache.keys()[:cutting_point]:
                            del cached._cache[key]
                            
                @misc_tools.set_attributes(_cache=OrderedDict())        
                def cached(function, *args, **kwargs):
                    remove_expired_entries()
                    sleek_call_args = \
                        SleekCallArgs(cached._cache, function, *args, **kwargs)
                    try:
                        return cached._cache[sleek_call_args][0]
                    except KeyError:
                        value = function(*args, **kwargs)
                        cached._cache[sleek_call_args] = (
                            value,
                            _get_now() + time_to_keep
                        )
                        cached._cache.sort(key=sorting_key_function)
                        return value
                
            else: # not time_to_keep
                
                @misc_tools.set_attributes(_cache={})        
                def cached(function, *args, **kwargs):
                    sleek_call_args = \
                        SleekCallArgs(cached._cache, function, *args, **kwargs)
                    try:
                        return cached._cache[sleek_call_args]
                    except KeyError:
                        cached._cache[sleek_call_args] = value = \
                              function(*args, **kwargs)
                        return value
    
        else: # max_size < infinity
            
            @misc_tools.set_attributes(_cache=OrderedDict())        
            def cached(function, *args, **kwargs):
                sleek_call_args = \
                    SleekCallArgs(cached._cache, function, *args, **kwargs)
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
                    
        
        result = decorator_tools.decorator(cached, function)
        
        def cache_clear(key=CLEAR_ENTIRE_CACHE):
            if key is CLEAR_ENTIRE_CACHE:
                cached._cache.clear()
            else:
                try:
                    del cached._cache[key]
                except KeyError:
                    pass
                
        result.cache_clear = cache_clear
        
        result.is_cached = True
        
        return result
        
    return decorator

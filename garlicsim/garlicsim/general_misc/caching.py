
# todo: use this in all the places where i `get` shit in garlicsim_wx, like
# get_background_brush

import functools

def cache(function):
    # todo: kwargs support
    # todo: try to be smart and figure out the function's signature, then be
    # able to understand that squared(x) is the same as sqaured(number=x).
    if hasattr(function, 'cache'): return function
    
    def cached(*args):
        
        try:
            return cached.cache[args]
        except KeyError:
            cached.cache[args] = value = function(*args)
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

        value = self.getter(obj)
        
        if not self.our_name:
            if not our_type:
                our_type = type(obj)
            (self.our_name,) = (key for (key, value) in 
                                vars(our_type).iteritems()
                                if value is self)
        
        setattr(obj, self.our_name, value)
        
        return value

    
        
    
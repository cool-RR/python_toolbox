# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''
Defines the `CachedProperty` class.

See its documentation for more details.
'''

from python_toolbox import decorator_tools
from python_toolbox import misc_tools


class CachedProperty(misc_tools.OwnNameDiscoveringDescriptor):
    '''
    A property that is calculated only once for an object, and then cached.
    
    Usage:
    
        class MyObject:
        
            # ... Regular definitions here
        
            def _get_personality(self):
                print('Calculating personality...')
                time.sleep(5) # Time consuming process that creates personality
                return 'Nice person'
        
            personality = CachedProperty(_get_personality)
            
    You can also put in a value as the first argument if you'd like to have it
    returned instead of using a getter. (It can be a totally static value like
    `0`). If this value happens to be a callable but you'd still like it to be
    used as a static value, use `force_value_not_getter=True`.
    '''
    def __init__(self, getter_or_value, doc=None, name=None,
                 force_value_not_getter=False):
        '''
        Construct the cached property.
        
        `getter_or_value` may be either a function that takes the parent object
        and returns the value of the property, or the value of the property
        itself, (as long as it's not a callable.)
        
        You may optionally pass in the name that this property has in the
        class; this will save a bit of processing later.
        '''
        misc_tools.OwnNameDiscoveringDescriptor.__init__(self, name=name)
        if callable(getter_or_value) and not force_value_not_getter:
            self.getter = getter_or_value
        else:
            self.getter = lambda thing: getter_or_value
        self.__doc__ = doc or getattr(self.getter, '__doc__', None)
        
        
    def __get__(self, thing, our_type=None):

        if thing is None:
            # We're being accessed from the class itself, not from an object
            return self
        
        value = self.getter(thing)
        
        setattr(thing, self.get_our_name(thing, our_type=our_type), value)
        
        return value

    
    def __call__(self, method_function):
        '''
        Decorate method to use value of `CachedProperty` as a context manager.
        '''
        def inner(same_method_function, self_obj, *args, **kwargs):
            with getattr(self_obj, self.get_our_name(self_obj)):
                return method_function(self_obj, *args, **kwargs)
        return decorator_tools.decorator(inner, method_function)


    def __repr__(self):
        return '<%s: %s>' % (type(self).__name__, self.our_name or self.getter)
        
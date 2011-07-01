# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `CachedProperty` class.

See its documentation for more details.
'''

from garlicsim.general_misc import misc_tools


class CachedProperty(misc_tools.OwnNameDiscoveringProperty):
    '''
    A property that is calculated (a) lazily and (b) only once for an object.
    
    Usage:
    
        class MyObject(object):
        
            # ... Regular definitions here
        
            def _get_personality(self):
                print('Calculating personality...')
                time.sleep(5) # Time consuming process that creates personality
                return 'Nice person'
        
            personality = CachedProperty(_get_personality)
    
    '''
    def __init__(self, getter_or_value, doc=None, name=None):
        '''
        Construct the cached property.
        
        `getter_or_value` may be either a function that takes the parent object
        and returns the value of the property, or the value of the property
        itself, (as long as it's not a callable.)
        
        You may optionally pass in the name that this property has in the
        class; this will save a bit of processing later.
        '''
        misc_tools.OwnNameDiscoveringProperty.__init__(self, name=name)
        self.getter = getter_or_value if callable(getter_or_value) \
                      else lambda thing: getter_or_value
        self.__doc__ = doc or getattr(self.getter, '__doc__', None)
        
        
    def __get__(self, obj, our_type=None):

        if obj is None:
            # We're being accessed from the class itself, not from an object
            return self
        
        value = self.getter(obj)
        
        setattr(obj, self.get_our_name(obj, our_type=our_type), value)
        
        return value

    

# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

import re


class ProxyProperty:
    '''
    Property that serves as a proxy to an attribute of the parent object.
    
    When you create a `ProxyProperty`, you pass in the name of the attribute
    (or nested attribute) that it should proxy. (Prefixed with a dot.) Then,
    every time the property is `set`ed or `get`ed, the attribute is `set`ed or
    `get`ed instead.
    
    Example:
    
        class Chair:
        
            def __init__(self, whatever):
                self.whatever = whatever
                
            whatever_proxy = ProxyProperty('.whatever')
            
        chair = Chair(3)
        
        assert chair.whatever == chair.whatever_proxy == 3
        chair.whatever_proxy = 4
        assert chair.whatever == chair.whatever_proxy == 4
                
                
    You may also refer to a nested attribute of the object rather than a direct
    one; for example, you can do `ProxyProperty('.whatever.x.height')` and it
    will access the `.height` attribute of the `.x` attribute of `.whatever`.
    '''

    def __init__(self, attribute_name, doc=None):
        '''
        Construct the `ProxyProperty`.
        
        `attribute_name` is the name of the attribute that we will proxy,
        prefixed with a dot, like '.whatever'.
        
        You may also refer to a nested attribute of the object rather than a
        direct one; for example, you can do
        `ProxyProperty('.whatever.x.height')` and it will access the `.height`
        attribute of the `.x` attribute of `.whatever`.
        
        You may specify a docstring as `doc`.
        '''
        if not attribute_name.startswith('.'):
            raise Exception("The `attribute_name` must start with a dot to "
                            "make it clear it's an attribute. %s does not "
                            "start with a dot." % repr(attribute_name))
        self.getter = self.setter = None
        exec('def getter(thing): return thing%s' % attribute_name)
        exec('def setter(thing, value): thing%s = value' % attribute_name)
        exec('self.getter, self.setter = getter, setter')
        self.attribute_name = attribute_name[1:]
        self.__doc__ = doc
        
        
    def __get__(self, thing, our_type=None):
        if thing is None:
            # We're being accessed from the class itself, not from an object
            return self
        else:
            return self.getter(thing)
        
    def __set__(self, thing, value):
        # todo: should I check if `thing` is `None` and set on class? Same for
        # `__delete__`?
        
        return self.setter(thing, value)
        
    def __repr__(self):
        return '<%s: %s%s>' % (
            type(self).__name__,
            repr('.%s' % self.attribute_name),
            ', doc=%s' % repr(self.__doc__) if self.__doc__ else ''
        )
        
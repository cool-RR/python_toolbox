# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

import re

from .misc_tools import OwnNameDiscoveringDescriptor


class OverridableProperty(OwnNameDiscoveringDescriptor):
    '''
    blocktododoc
    '''
    
    def __init__(self, fget, doc=None, name=None):
        '''
        blocktododoc Construct the `ProxyProperty`.
        
        `attribute_name` is the name of the attribute that we will proxy,
        prefixed with a dot, like '.whatever'.
        
        You may also refer to a nested attribute of the object rather than a
        direct one; for example, you can do
        `ProxyProperty('.whatever.x.height')` and it will access the `.height`
        attribute of the `.x` attribute of `.whatever`.
        
        You may specify a docstring as `doc`.
        '''
        OwnNameDiscoveringDescriptor.__init__(name=name)
        if not attribute_name.startswith('.'):
            raise Exception("The `attribute_name` must start with a dot to "
                            "make it clear it's an attribute. %s does not "
                            "start with a dot." % repr(attribute_name))
        self.getter = fget
        self.__doc__ = doc
        
        
    def __get__(self, thing, our_type=None):
        if thing is None:
            # We're being accessed from the class itself, not from an object
            return self
        else:
            return self.getter(thing)
        
    def __set__(self, thing, value):
        setattr(thing, self.get_our_name(thing), value)
        
    def __repr__(self):
        return '<%s: %s>' % (type(self).__name__, self.our_name or self.getter)

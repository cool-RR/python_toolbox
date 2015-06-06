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
        OwnNameDiscoveringDescriptor.__init__(self, name=name)
        self.getter = fget
        self.__doc__ = doc
        
    def _get_overridden_attribute_name(self, thing):
        return '_%s__%s' % (type(self).__name__, self.get_our_name(thing))
        
        
    def __get__(self, thing, our_type=None):
        if thing is None:
            # We're being accessed from the class itself, not from an object
            return self
        else:
            overridden_attribute_name = self._get_overridden_attribute_name(thing)
            if hasattr(thing, overridden_attribute_name):
                return getattr(thing, overridden_attribute_name)
            else:
                return self.getter(thing)
        
    def __set__(self, thing, value):
        setattr(thing, self._get_overridden_attribute_name(thing), value)
        
    def __repr__(self):
        return '<%s: %s>' % (type(self).__name__, self.our_name or self.getter)

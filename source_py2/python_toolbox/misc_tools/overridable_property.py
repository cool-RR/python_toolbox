# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import re

from .misc_tools import OwnNameDiscoveringDescriptor


class OverridableProperty(OwnNameDiscoveringDescriptor):
    '''
    A property which may be overridden.

    This behaves exactly like the built-in `property`, except if you want to
    manually override the value of the property, you can. Example:

        >>> class Thing:
        ...     cat = OverridableProperty(lambda self: 'meow')
        ...
        >>> thing = Thing()
        >>> thing.cat
        'meow'
        >>> thing.cat = 'bark'
        >>> thing.cat
        'bark'

    '''

    def __init__(self, fget, doc=None, name=None):
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

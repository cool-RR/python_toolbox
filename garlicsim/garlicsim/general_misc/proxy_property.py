# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `` class.

See its documentation for more information.
'''

#blocktodo: allow doc
class ProxyProperty(object):
    def __init__(self, attribute_name):
        self.attribute_name = attribute_name
        
    def __get__(self, obj, our_type=None):
        if obj is None:
            # We're being accessed from the class itself, not from an object
            return self
        else:
            getattr(obj, self.attribute_name)
        
    def __set__(self, obj, value):
        setattr(obj, self.attribute_name, value)
        # blocktodo: should I check if obj is None and set on class?
        # Same for __delete__?
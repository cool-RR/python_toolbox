# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `ProxyProperty` class.

See its documentation for more information.
'''

from garlicsim.general_misc import address_tools


#blocktodo: allow doc
class ProxyProperty(object):
    def __init__(self, attribute_name, doc=None):
        '''
        blocktododoc: attribute can have dot in it.
        '''
        self.attribute_name = attribute_name
        self.__doc__ = doc
        
        
    def __get__(self, obj, our_type=None):
        if obj is None:
            # We're being accessed from the class itself, not from an object
            return self
        else:
            if '.' in self.attribute_name:
                return address_tools.resolve('obj.%s' % self.attribute_name,
                                             namespace={'obj': obj})
            else:
                return getattr(obj, self.attribute_name)
        
    def __set__(self, obj, value):
        
        
        # blocktodo: should I check if obj is None and set on class?
        # Same for __delete__?
        
        if '.' in self.attribute_name:
            left_segment, right_segment = self.attribute_name.rsplit('.', 1)
            deepest_object = address_tools.resolve('obj.%s' % left_segment,
                                                   namespace={'obj': obj})
            setattr(deepest_object, right_segment, value)
        else:
            setattr(obj, self.attribute_name, value)
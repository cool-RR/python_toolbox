# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

'''
This module defines the `ProxyProperty` class.

See its documentation for more information.
'''

import re

simple_case_pattern = re.compile(r'''([A-Za-z0-9_]+\.?)+''')


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
        self.attribute_name = attribute_name[1:]
        self.__doc__ = doc
        
        
    def __get__(self, obj, our_type=None):
        if obj is None:
            # We're being accessed from the class itself, not from an object
            return self
        else:
            if simple_case_pattern.match(self.attribute_name):
                current_object = obj
                for attribute_name in self.attribute_name.split('.'):
                    current_object = getattr(current_object, attribute_name)
                return current_object
            else:
                from python_toolbox import address_tools
                return address_tools.resolve('obj.%s' % self.attribute_name,
                                             namespace={'obj': obj})
        
    def __set__(self, obj, value):
        
        # todo: should I check if `obj` is `None` and set on class? Same for
        # `__delete__`?
        
        if simple_case_pattern.match(self.attribute_name):
            current_object = obj
            for attribute_name in self.attribute_name.split('.')[:-1]:
                current_object = getattr(current_object, attribute_name)
            setattr(current_object, self.attribute_name.split('.')[-1], value)
        else:
            from python_toolbox import address_tools
            left_segment, right_segment = self.attribute_name.rsplit('.', 1)
            deepest_object = address_tools.resolve('obj.%s' % left_segment,
                                                   namespace={'obj': obj})
            setattr(deepest_object, right_segment, value)

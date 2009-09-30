# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

"""
This module defines the CoolDict class. See its documentation for more
information.
"""

import copy

class CoolDict(dict):
    """
    A class derived from dict which some extra methods.
    """
    def raise_to(self, key, value):
        """
        Same as `cool_dict[key] = value`, except if the cool dict already has
        `key`, and its value is higher than `value`.
        """
        has_key = self.has_key(key)
        if not has_key:
            self[key] = value
        else:
            self[key] = max(value, self[key])
            
    def lower_to(self, key, value):
        """
        Same as `cool_dict[key] = value`, except if the cool dict already has
        `key`, and its value is lower than `value`.
        """
        has_key = self.has_key(key)
        if not has_key:
            self[key] = value
        else:
            self[key] = min(value, self[key])
            
    def copy(self):
        return CoolDict(self)
    
    def __copy__(self):
        return CoolDict(self)
    
    def __deepcopy__(self, memo):
        raise NotImplementedError # todo
    
    def transfer_value(self, key, new_key):
        assert self.has_key(key)
        assert not self.has_key(new_key)
        
        value = self[key]
        self[new_key] = value
        del self[key]
        
        return value
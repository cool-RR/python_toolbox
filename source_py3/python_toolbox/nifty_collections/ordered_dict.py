# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''
This module defines the `OrderedDict` class.

See its documentation for more information.
'''

from python_toolbox import comparison_tools

from collections import OrderedDict as StdlibOrderedDict


class OrderedDict(StdlibOrderedDict):
    
    def sort(self, key=None, reversed=False):
        '''
        Sort the items according to their keys, changing the order in-place.
        
        The optional `key` argument, (not to be confused with the dictionary
        keys,) will be passed to the `sorted` function as a key function.
        '''
        key_function = \
                   comparison_tools.process_key_function_or_attribute_name(key)
        sorted_keys = sorted(self.keys(), key=key_function)
        step = -1 if reversed else 1
        for key_ in sorted_keys[1::step]:
            self.move_to_end(key_)
        
    
    def index(self, key):
        '''Get the index number of `key`.'''
        if key not in self:
            raise KeyError
        for i, key_ in enumerate(self):
            if key_ == key:
                return i
        raise RuntimeError
                
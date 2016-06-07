# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import sys_tools
from python_toolbox import comparison_tools

try:
    from collections import OrderedDict as StdlibOrderedDict
except ImportError:
    from python_toolbox.third_party.collections import OrderedDict \
                                                           as StdlibOrderedDict


class OrderedDict(StdlibOrderedDict):
    '''
    A dictionary with an order.
    
    This is a subclass of `collections.OrderedDict` with a couple of
    improvements.
    '''
    
    def move_to_end(self, key, last=True):
        '''Move an existing element to the end (or beginning if last==False).

        Raises KeyError if the element does not exist.
        When last=True, acts like a fast version of self[key]=self.pop(key).

        '''
        try:
            self.__map
        except AttributeError: # PyPy
            if last:
                self[key] = self.pop(key)
            else:
                # Very inefficient implementation for corner case.
                value = self.pop(key)
                items = tuple(self.items())
                self.clear()
                self[key] = value
                self.update(items)
            return
        else:
            link = self.__map[key]
            link_prev = link[0]
            link_next = link[1]
            link_prev[1] = link_next
            link_next[0] = link_prev
            root = self.__root
            if last:
                last = self.__root[0]
                link[0] = last
                link[1] = self.__root
                last[1] = self.__root[0] = link
            else:
                first = self.__root[1]
                link[0] = self.__root
                link[1] = first
                root[1] = first[0] = link
            

    def sort(self, key=None, reverse=False):
        '''
        Sort the items according to their keys, changing the order in-place.
        
        The optional `key` argument, (not to be confused with the dictionary
        keys,) will be passed to the `sorted` function as a key function.
        '''
        key_function = \
                   comparison_tools.process_key_function_or_attribute_name(key)
        sorted_keys = sorted(self.keys(), key=key_function, reverse=reverse)
        for key_ in sorted_keys[1:]:
            self.move_to_end(key_)
        
    
    def index(self, key):
        '''Get the index number of `key`.'''
        if key not in self:
            raise ValueError
        for i, key_ in enumerate(self):
            if key_ == key:
                return i
        raise RuntimeError
    
    @property
    def reversed(self):
        '''Get a version of this `OrderedDict` with key order reversed.'''
        return type(self)(reversed(tuple(self.items())))
# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import comparison_tools

from collections import OrderedDict as StdlibOrderedDict


class OrderedDict(StdlibOrderedDict):
    '''
    A dictionary with an order.

    This is a subclass of `collections.OrderedDict` with a couple of
    improvements.
    '''

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
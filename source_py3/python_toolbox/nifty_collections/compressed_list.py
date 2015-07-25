# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

import collections
import itertools


class CompressedList(collections.MutableSequence):
    def __init__(self, iterable=()):
        self._clear()
        self.extend(iterable)
        
    def _clear(self):
        self._list = []
        
    def extend(self, iterable):
        last_item_in_list = self._list[-1][1] if self._list else object()
        for item in iterable:
            if item is last_item_in_list:
                self._list[-1][0] += 1
            else:
                self._list.append([1, item])
                last_item_in_list = item
        
    def __iter__(self):
        for count, item in self._list:
            for _ in range(count):
                yield item
                
    def __getitem__(self, i):
        if isinstance(i, int):
            raise NotImplementedError
        elif isinstance(i, slice):
            raise NotImplementedError
        else:
            raise Exception
        
    def __delitem__(self, i):
        raise NotImplementedError
    
    def __setitem__(self, i, value):
        raise NotImplementedError
    
    def __len__(self):
        raise NotImplementedError
    
    def insert(self, i, thing):
        raise NotImplementedError
        
    
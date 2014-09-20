# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

import collections

from python_toolbox import comparison_tools
from python_toolbox import misc_tools

from .ordered_set import OrderedSet, KEY, PREV, NEXT


class SortedSet(OrderedSet):
    
    def __init__(self, iterable=None, key=None, reverse=False):
        super().__init__(iterable=iterable)
        self._key = key if (key is not None) else misc_tools.identity_function
        self._reverse = reverse
        

    _sort = lambda self: self.sort(key=self._key, reverse=self._reverse)

    def add(self, key):
        """
        Add an element to a set.
    
        This has no effect if the element is already present.
        """
        super().add(key)
        self._sort()
        
        
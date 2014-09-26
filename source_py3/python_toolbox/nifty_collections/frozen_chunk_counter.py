# Copyright 2009-2014 Ram Rachum.,
# This program is distributed under the MIT license.

import collections

from python_toolbox import math_tools

from .frozen_counter import FrozenCounter


class FrozenChunkCounter(FrozenCounter):
    def __init__(self, iterable):
        super().__init__(iterable)
        
        # All zero values were already fileterd out by `FrozenCounter`, we'll
        # filter out just the non-natural-number keys.
        for key in [key for key in self if not isinstance(key, math_tools.Natural)]:
            if key == 0:
                del self._dict[key]
            else:
                raise TypeError('Keys to `FrozenChunkCounter` must be '
                                'non-negative integers.')
            
    def get_sub_counters_counter(self):
        sub_counters_counter = collections.Counter()
        for key_to_reduce, value_of_key_to_reduce in self.items():
            sub_counter = collections.Counter(self)
            sub_counter[key_to_reduce] -= 1
            sub_counter[key_to_reduce - 1] += 1
            sub_counters_counter[FrozenChunkCounter(sub_counter)] = \
                                                         value_of_key_to_reduce
        return FrozenCounter(sub_counters_counter)
            

# Copyright 2009-2014 Ram Rachum.,
# This program is distributed under the MIT license.

from python_toolbox import math_tools

from .frozen_counter import FrozenCounter


class FrozenChunkCounter(FrozenCounter):
    def __init__(self, iterable):
        super().__init__()
        
        # All zero values were already fileterd out by `FrozenCounter`, we'll
        # filter out just the non-natural-number keys.
        for key in [key for key in self if not isinstance(key, math_tools.Natural)]:
            if key == 0:
                del self._dict[key]
            else:
                raise TypeError('Keys to `FrozenChunkCounter` must be '
                                'non-negative integers.')

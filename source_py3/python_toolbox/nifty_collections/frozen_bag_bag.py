# Copyright 2009-2014 Ram Rachum.,
# This program is distributed under the MIT license.

import collections

from python_toolbox import math_tools

from .bagging import FrozenBag


class FrozenBagBag(FrozenBag):
    '''
    
    
    blocktododoc do entire crate metaphor with drawings. say that crates of the same pile are identical.
    '''
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
            
    def get_sub_fbbs_for_one_crate_removed(self):
        sub_fbbs_counter = collections.Counter()
        for key_to_reduce, value_of_key_to_reduce in self.items():
            sub_fbb_prototype = collections.Counter(self)
            sub_fbb_prototype[key_to_reduce] -= 1
            sub_fbb_prototype[key_to_reduce - 1] += 1
            sub_fbbs_counter[FrozenBagBag(sub_fbb_prototype)] = \
                                                         value_of_key_to_reduce
        return FrozenBag(sub_fbbs_counter)
            
    def get_sub_fbbs_for_one_crate_and_previous_piles_removed(self):
        sub_fbbs = []
        growing_dict = {}
        for key_to_reduce, value_of_key_to_reduce in \
                                                reversed(sorted(self.items())):
            growing_dict[key_to_reduce] = value_of_key_to_reduce
            
            sub_fbb_prototype = collections.Counter(growing_dict)
            sub_fbb_prototype[key_to_reduce] -= 1
            sub_fbb_prototype[key_to_reduce - 1] += 1
            
            for i in range(value_of_key_to_reduce):
                sub_fbbs.append(
                    FrozenBagBag(
                        {key: (i if key == key_to_reduce else value)
                               for key, value in sub_fbb_prototype.items()}
                    )
                )
        return tuple(sub_fbbs)
            
    

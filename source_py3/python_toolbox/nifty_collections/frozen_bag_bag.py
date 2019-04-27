# Copyright 2009-2017 Ram Rachum.,
# This program is distributed under the MIT license.

import collections

from python_toolbox import math_tools

from .bagging import Bag, FrozenBag


class FrozenBagBag(FrozenBag):
    '''
    A bag where a key is the number of recurrences of an item in another bag.

    A `FrozenBagBag` is usually created as a property of another bag or
    container. If the original bag has 3 different items that have a count of 2
    each, then this `FrozenBagBag` would have the key-value pair `2: 3`. Note
    that the original keys are not saved here, only their number of
    recurrences.

    Example:

        >>> bag = Bag('abracadabra')
        >>> bag
        Bag({'b': 2, 'r': 2, 'a': 5, 'd': 1, 'c': 1})
        >>> bag.frozen_bag_bag
        FrozenBagBag({1: 2, 2: 2, 5: 1})

    '''
    def __init__(self, iterable):
        super().__init__(iterable)

        # All zero values were already fileterd out by `FrozenBag`, we'll
        # filter out just the non-natural-number keys.
        for key in [key for key in self if not isinstance(key, math_tools.Natural)]:
            if key == 0:
                del self._dict[key]
            else:
                raise TypeError('Keys to `FrozenBagBag` must be '
                                'non-negative integers.')

    def get_sub_fbbs_for_one_key_removed(self):
        '''
        Get all FBBs that are like this one but with one key removed.

        We're talking about a key from the original bag, not from the FBB.

        Example:

            >>> fbb = FrozenBagBag({2: 3, 3: 10})
            >>> fbb.get_sub_fbbs_for_one_key_removed()
            FrozenBag({FrozenBagBag({1: 1, 2: 2, 3: 10}): 3,
                       FrozenBagBag({2: 4, 3: 9}): 10})

        The results come in a `FrozenBag`, where each count is the number of
        different options for making that sub-FBB.
        '''
        sub_fbbs_bag = Bag()
        for key_to_reduce, value_of_key_to_reduce in self.items():
            sub_fbb_prototype = Bag(self)
            sub_fbb_prototype[key_to_reduce] -= 1
            sub_fbb_prototype[key_to_reduce - 1] += 1
            sub_fbbs_bag[FrozenBagBag(sub_fbb_prototype)] = \
                                                         value_of_key_to_reduce
        return FrozenBag(sub_fbbs_bag)

    def get_sub_fbbs_for_one_key_and_previous_piles_removed(self):
        '''
        Get all sub-FBBs with one key and previous piles removed.

        What does this mean? First, we organize all the items in arbitrary
        order. Then we go over the piles (e.g. an item of `2: 3` is three piles
        with 2 crates each), and for each pile we make an FBB that has all the
        piles in this FBB except it has one item reduced from the pile we
        chose, and it doesn't have all the piles to its left.

            >>> fbb = FrozenBagBag({2: 3, 3: 10})
            >>> fbb.get_sub_fbbs_for_one_key_and_previous_piles_removed()
            (FrozenBagBag({2: 1}),
             FrozenBagBag({2: 1, 3: 1}),
             FrozenBagBag({2: 1, 3: 2}),
             FrozenBagBag({2: 1, 3: 3}),
             FrozenBagBag({2: 1, 3: 4}),
             FrozenBagBag({2: 1, 3: 5}),
             FrozenBagBag({2: 1, 3: 6}),
             FrozenBagBag({2: 1, 3: 7}),
             FrozenBagBag({2: 1, 3: 8}),
             FrozenBagBag({2: 1, 3: 9}),
             FrozenBagBag({1: 1, 3: 10}),
             FrozenBagBag({1: 1, 2: 1, 3: 10}),
             FrozenBagBag({1: 1, 2: 2, 3: 10}))

        '''
        sub_fbbs = []
        growing_dict = {}
        for key_to_reduce, value_of_key_to_reduce in \
                                                reversed(sorted(self.items())):
            growing_dict[key_to_reduce] = value_of_key_to_reduce

            sub_fbb_prototype = Bag(growing_dict)
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



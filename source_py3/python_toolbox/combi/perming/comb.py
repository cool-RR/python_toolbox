# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

from .perm import Perm, UnrecurrentedPerm
from .comb_space import CombSpace


class Comb(Perm):
    '''
    A combination of items from a `CombSpace`.

    In combinatorics, a combination is like a permutation except with no order.
    In the `combi` package, we implement that by making the items in `Comb` be
    in canonical order. (This has the same effect as having no order because
    each combination of items can only appear once, in the canonical order,
    rather than many different times in many different orders like with
    `Perm`.)

    Example:

        >>> comb_space = CombSpace('abcde', 3)
        >>> comb = Comb('bcd', comb_space)
        >>> comb
        <Comb, n_elements=3: ('a', 'b', 'c')>
        >>> comb_space.index(comb)
        6

    '''
    def __init__(self, perm_sequence, perm_space=None):
        # Unlike for `Perm`, we must have a `perm_space` in the arguments. It
        # can either be in the `perm_space` argument, or if the `perm_sequence`
        # we got is a `Comb`, then we'll take the one from it.
        assert isinstance(perm_space, CombSpace) or \
                                                isinstance(perm_sequence, Comb)

        Perm.__init__(self, perm_sequence=perm_sequence,
                      perm_space=perm_space)


class UnrecurrentedComb(UnrecurrentedPerm, Comb):
    '''A combination in a space that's been unrecurrented.'''





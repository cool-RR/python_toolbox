# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import collections

from python_toolbox import sequence_tools


class SelectionSpace(sequence_tools.CuteSequenceMixin,
                     collections.abc.Sequence):
    '''
    Space of possible selections of any number of items from `sequence`.

    For example:

        >>> tuple(SelectionSpace(range(2)))
        (set(), {1}, {0}, {0, 1})

    The selections (which are sets) can be for any number of items, from zero
    to the length of the sequence.

    Of course, this is a smart object that doesn't really create all these sets
    in advance, but rather on demand. So you can create a `SelectionSpace` like
    this:

        >>> selection_space = SelectionSpace(range(10**4))

    And take a random selection from it:

        >>> selection_space.take_random()
        {0, 3, 4, ..., 9996, 9997}

    Even though the length of this space is around 10 ** 3010, which is much
    bigger than the number of particles in the universe.
    '''
    def __init__(self, sequence):
        self.sequence = \
             sequence_tools.ensure_iterable_is_immutable_sequence(sequence)
        self.sequence_length = len(self.sequence)
        self._sequence_set = set(self.sequence)
        self.length = 2 ** self.sequence_length


    def __repr__(self):
        return '<%s: %s>' % (
            type(self).__name__,
            self.sequence
        )


    def __getitem__(self, i):
        if isinstance(i, slice):
            raise NotImplementedError

        if (-self.length <= i <= -1):
            i += self.length
        if not (0 <= i < self.length):
            raise IndexError

        pattern = '{0:0%sb}' % self.sequence_length
        binary_i = pattern.format(i)

        assert len(binary_i) == self.sequence_length

        return set(item for (is_included, item) in
                   zip(map(int, binary_i), self.sequence) if is_included)


    _reduced = property(lambda self: (type(self), self.sequence))
    __hash__ = lambda self: hash(self._reduced)
    __bool__ = lambda self: bool(self.length)
    __eq__ = lambda self, other: (isinstance(other, SelectionSpace) and
                                  self._reduced == other._reduced)

    def index(self, selection):
        '''Find the index number of `selection` in this `SelectionSpace`.'''
        if not isinstance(selection, collections.abc.Iterable):
            raise ValueError

        selection_set = set(selection)

        if not selection_set <= self._sequence_set:
            raise ValueError

        return sum((2 ** i) for i, item in enumerate(reversed(self.sequence))
                                                 if item in selection_set)






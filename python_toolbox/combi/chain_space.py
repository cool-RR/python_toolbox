# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

from __future__ import generator_stop

import collections

from python_toolbox import binary_search
from python_toolbox import nifty_collections
from python_toolbox import caching

from python_toolbox import sequence_tools
from python_toolbox import nifty_collections

infinity = float('inf')



class ChainSpace(sequence_tools.CuteSequenceMixin, collections.abc.Sequence):
    '''
    A space of sequences chained together.

    This is similar to `itertools.chain`, except that items can be fetched by
    index number rather than just iteration.

    Example:

        >>> chain_space = ChainSpace(('abc', (1, 2, 3)))
        >>> chain_space
        <ChainSpace: 3+3>
        >>> chain_space[4]
        2
        >>> tuple(chain_space)
        ('a', 'b', 'c', 1, 2, 3)
        >>> chain_space.index(2)
        4

    '''
    def __init__(self, sequences):
        self.sequences = nifty_collections.LazyTuple(
            (sequence_tools.ensure_iterable_is_immutable_sequence(
                sequence, default_type=nifty_collections.LazyTuple)
                                                     for sequence in sequences)
        )

    @caching.CachedProperty
    @nifty_collections.LazyTuple.factory()
    def accumulated_lengths(self):
        '''
        A sequence of the accumulated length as every sequence is added.

        For example, if this chain space has sequences with lengths of 10, 100
        and 1000, this would be `[0, 10, 110, 1110]`.
        '''
        total = 0
        yield 0
        for sequence in self.sequences:
            total += sequence_tools.get_length(sequence)
            yield total


    length = caching.CachedProperty(lambda self: self.accumulated_lengths[-1])

    def __repr__(self):
        return '<%s: %s>' % (
            type(self).__name__,
            '+'.join(str(len(sequence)) for sequence in self.sequences),
        )

    def __getitem__(self, i):
        if isinstance(i, slice):
            raise NotImplementedError
        assert isinstance(i, int)
        if i <= -1:
            i += self.length
        if i < 0:
            raise IndexError
        if self.accumulated_lengths.is_exhausted and i >= self.length:
            raise IndexError
        # Todo: Can't have a binary search here, it exhausts all the sequences.
        sequence_index = binary_search.binary_search_by_index(
            self.accumulated_lengths, i, rounding=binary_search.LOW_IF_BOTH
        )
        if sequence_index is None:
            raise IndexError
        sequence_start = self.accumulated_lengths[sequence_index]
        return self.sequences[sequence_index][i - sequence_start]


    def __iter__(self):
        for sequence in self.sequences:
            yield from sequence

    _reduced = property(lambda self: (type(self), self.sequences))

    __eq__ = lambda self, other: (isinstance(other, ChainSpace) and
                                  self._reduced == other._reduced)

    def __contains__(self, item):
        return any(item in sequence for sequence in self.sequences
                   if (not isinstance(sequence, str) or isinstance(item, str)))

    def index(self, item):
        '''Get the index number of `item` in this space.'''
        for sequence, accumulated_length in zip(self.sequences,
                                                self.accumulated_lengths):
            try:
                index_in_sequence = sequence.index(item)
            except ValueError:
                pass
            except TypeError:
                assert isinstance(sequence, (str, bytes)) and \
                                           (not isinstance(item, (str, bytes)))
            else:
                return index_in_sequence + accumulated_length
        else:
            raise ValueError

    def __bool__(self):
        try: next(iter(self))
        except StopIteration: return False
        else: return True


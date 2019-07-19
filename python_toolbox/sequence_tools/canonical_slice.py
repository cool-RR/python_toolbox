# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import collections

from python_toolbox import math_tools

infinity = float('inf')
infinities = (infinity, -infinity)


class CanonicalSlice:
    '''
    A canonical representation of a `slice` with `start`, `stop`, and `step`.

    This is helpful because `slice`'s own `.start`, `.stop` and `.step` are
    sometimes specified as `None` for convenience, so Python will infer them
    automatically. Here we make them explicit. If we're given an iterable (or
    the length of one) in `iterable_or_length`, we'll give a canoncial slice
    for that length, otherwise we'll do a generic one, which is rarely usable
    for actual slicing because it often has `infinity` in it, so it's useful
    only for canonalization. (e.g. checking whether two different slices are
    actually equal.)

    When doing a generic canonical slice (without giving an iterable or
    length):

      - If `start` is `None`, it will be set to `0` (if the `step` is positive)
        or `infinity` (if the `step` is negative.)

      - If `stop` is `None`, it will be set to `infinity` (if the `step` is
        positive) or `0` (if the `step` is negative.)

      - If `step` is `None`, it will be changed to the default `1`.

    '''

    def __init__(self, slice_, iterable_or_length=None, offset=0):
        from python_toolbox import sequence_tools
        from python_toolbox import cute_iter_tools

        if isinstance(slice_, CanonicalSlice):
            slice_ = slice(slice_.start, slice_.stop, slice_.step)
        assert isinstance(slice_, slice)
        self.given_slice = slice_
        if iterable_or_length is not None:
            if isinstance(iterable_or_length,
                          math_tools.PossiblyInfiniteIntegral):
                self.length = iterable_or_length
            elif isinstance(iterable_or_length, collections.abc.Sequence):
                self.length = sequence_tools.get_length(iterable_or_length)
            else:
                assert isinstance(iterable_or_length, collections.abc.Iterable)
                self.length = cute_iter_tools.get_length(iterable_or_length)
        else:
            self.length = None

        self.offset = offset

        ### Parsing `step`: ###################################################
        #                                                                     #
        assert slice_.step != 0
        if slice_.step is None:
            self.step = 1
        else:
            self.step = slice_.step
        #                                                                     #
        ### Finished parsing `step`. ##########################################


        ### Parsing `start`: #################################################
        #                                                                    #
        if slice_.start is None:
            if self.step > 0:
                self.start = 0 + self.offset
            else:
                assert self.step < 0
                self.start = (self.length + self.offset) if \
                                        (self.length is not None) else infinity
        else: # s.start is not None
            if self.length is not None:
                if slice_.start < 0:
                    self.start = \
                               max(slice_.start + self.length, 0) + self.offset
                else:
                    self.start = min(slice_.start, self.length) + self.offset
            else:
                self.start = slice_.start + self.offset
        #                                                                     #
        ### Finished parsing `start`. #########################################

        ### Parsing `stop`: ###################################################
        #                                                                     #
        if slice_.stop is None:
            if self.step > 0:
                self.stop = (self.length + self.offset) if \
                                        (self.length is not None) else infinity
            else:
                assert self.step < 0
                self.stop = -infinity

        else: # slice_.stop is not None
            if self.length is not None:
                if slice_.stop < 0:
                    self.stop = max(slice_.stop + self.length, 0) + self.offset
                else: # slice_.stop >= 0
                    self.stop = min(slice_.stop, self.length) + self.offset
            else:
                self.stop = slice_.stop + self.offset
        #                                                                     #
        ### Finished parsing `stop`. ##########################################

        if (self.step > 0 and self.start >= self.stop >= 0) or \
           (self.step < 0 and self.stop >= self.start):
            # We have a case of an empty slice.
            self.start = self.stop = 0


        self.slice_ = slice(*((item if item not in math_tools.infinities
                               else None) for item in self))

        ### Doing sanity checks: ##############################################
        #                                                                     #
        if self.length:
            if self.step > 0:
                assert 0 <= self.start <= \
                                         self.stop <= self.length + self.offset
            else:
                assert self.step < 0
                assert 0 <= self.stop <= \
                                        self.start <= self.length + self.offset
        #                                                                     #
        ### Finished doing sanity checks. #####################################

    __iter__ = lambda self: iter((self.start, self.stop, self.step))
    __repr__ = lambda self: f'{type(self).__name__}{tuple(self)}'
    _reduced = property(lambda self: (type(self), tuple(self)))
    __hash__ = lambda self: hash(self._reduced)
    __eq__ = lambda self, other: (isinstance(other, CanonicalSlice) and
                                  self._reduced == other._reduced)
    __contains__ = lambda self, number: self.start <= number < self.stop




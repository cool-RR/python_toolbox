# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `LazyList` class.

See its documentation for more information.
'''

import textwrap
from keyword import iskeyword
from operator import itemgetter
from functools import wraps
import itertools


class LazyList(object):
    ''' '''
    def __init__(self, iterable):
        was_given_a_sequence = isinstance(iterable, (list, tuple, basestring))
        self.exhausted = True if was_given_a_sequence else False
        if was_given_a_sequence:
            self._collected_data = list(iterable)
        else: # not was_given_a_sequence
            self._collected_data = []
            self._iterator = iter(iterable)
            
    def _exhaust(self, i=None):
        if self.exhausted:
            return
        elif i is None or i < 0:
            index_range = itertools.count(self.known_length)
        elif isinstance(i, slice):
            start, stop = i.start, i.stop
            if start < 0 or stop < 0:
                index_range = itertools.count(self.known_length)
            else:
                index_range = xrange(self.known_length, stop)
        else:
            index_range = xrange(self.known_length, i + 1)
        for i in index_range:
            try:
                self._collected_data.append(self._iterator.next())
            except StopIteration:
                self.exhausted = True
                break
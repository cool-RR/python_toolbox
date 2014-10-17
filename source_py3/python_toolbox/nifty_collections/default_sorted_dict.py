# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

import collections

from python_toolbox.third_party import sortedcontainers


class DefaultSortedDict(sortedcontainers.SortedDict):

    def __init__(self, default_factory, *args, **kwargs):
        assert isinstance(default_factory, collections.Callable)
        self.default_factory = default_factory
        sortedcontainers.SortedDict.__init__(self, *args, **kwargs)
  
    def copy(self):
        """ D.copy() -> a shallow copy of D. """
        return type(self)(self.default_factory, self.items())
  
    def __getitem__(self, key):
        try:
            return self._dict[key]
        except KeyError:
            return self.default_factory()
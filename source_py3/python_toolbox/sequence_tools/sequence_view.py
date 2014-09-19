import abc
import builtins
import types
import collections
import numbers

from python_toolbox import caching

from .misc import CuteSequence

infinity = float('inf')
infinities = (infinity, -infinity)


class SequenceView(CuteSequence):
    def __init__(self, sequence, indices=None):
        self.sequence = sequence
        if indices is not None:
            self.indices = indices

    indices = caching.CachedProperty(
                                  lambda self: list(range(len(self.sequence))))
        
    def __getitem__(self, index):
        return self.sequence[self.indices[index]]

    def __iter__(self):
        yield from map(self.sequence.__getitem__, self.indices)

    __contains__ = lambda self: any(item == value for value in self)

    def __reversed__(self):
        yield from map(self.sequence.__getitem__, reversed(self.indices))

    # Can't defined `index` which uses the wrapped sequence's `index` because
    # `index` stops on the first occurrence, and if our first occurrence was
    # removed, we'd need to search for the next one.

    def _nopity_nope_nope(self, item):
        raise TypeError("Can't add stuff to a `VirtualPopper`")
    extend = insert = append = _nopity_nope_nope
    
    clear = lambda self: self.sequence.clear()
    copy = lambda self: type(self)(self.sequence, indices=self.indices)
    reverse = lambda self: self.indices.reverse()
    
    # This are the money methods right here:
    pop = lambda self, i: self.sequence[self.indices.pop(i)]
    remove = lambda self, item: self.indices.remove(self.sequence.index(item))
    
        
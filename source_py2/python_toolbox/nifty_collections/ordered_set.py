# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''
Defines the `OrderedSet` class.

See its documentation for more details.
'''
# todo: revamp

import collections

KEY, PREV, NEXT = range(3)


class OrderedSet(collections.MutableSet):
    '''
    A set with an order.
    
    You can also think of this as a list which doesn't allow duplicate items
    and whose `__contains__` method is O(1).
    '''

    def __init__(self, iterable=None):
        self.end = end = [] 
        end += [None, end, end]         # sentinel node for doubly linked list
        self.map = {}                   # key --> [key, prev, next]
        if iterable is not None:
            self |= iterable

    def __len__(self):
        return len(self.map)

    def __contains__(self, key):
        return key in self.map

    def add(self, key):
        """
        Add an element to a set.
    
        This has no effect if the element is already present.
        """
        if key not in self.map:
            end = self.end
            curr = end[PREV]
            curr[NEXT] = end[PREV] = self.map[key] = [key, curr, end]

    def discard(self, key):
        """
        Remove an element from a set if it is a member.
    
        If the element is not a member, do nothing.
        """
        if key in self.map:        
            key, prev, next = self.map.pop(key)
            prev[NEXT] = next
            next[PREV] = prev

    def __iter__(self):
        end = self.end
        curr = end[NEXT]
        while curr is not end:
            yield curr[KEY]
            curr = curr[NEXT]

    def __reversed__(self):
        end = self.end
        curr = end[PREV]
        while curr is not end:
            yield curr[KEY]
            curr = curr[PREV]

    def pop(self, last=True):
        """Remove and return an arbitrary set element."""
        if not self:
            raise KeyError('set is empty')
        key = next(reversed(self) if last else iter(self))
        self.discard(key)
        return key

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)

    def __del__(self):
        self.clear()                    # remove circular references
        # todo: is this really needed? i'm worried about this making the gc not
        # drop circulary-referencing objects.

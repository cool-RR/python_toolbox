# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

from __future__ import generator_stop

import collections
import operator
import itertools

from python_toolbox import comparison_tools
from python_toolbox import context_management
from python_toolbox import caching
from python_toolbox import freezing



KEY, PREV, NEXT = range(3)


class BaseOrderedSet(collections.abc.Set, collections.abc.Sequence):
    '''
    Base class for `OrderedSet` and `FrozenOrderedSet`, i.e. set with an order.

    This behaves like a `set` except items have an order. (By default they're
    ordered by insertion order, but that order can be changed.)
    '''

    def __init__(self, iterable=()):
        self.__clear()
        for item in iterable:
            self.__add(item)

    def __getitem__(self, index):
        for i, item in enumerate(self):
            if i == index:
                return item
        else:
            raise IndexError

    def __len__(self):
        return len(self._map)

    def __contains__(self, key):
        return key in self._map


    def __iter__(self):
        end = self._end
        curr = end[NEXT]
        while curr is not end:
            yield curr[KEY]
            curr = curr[NEXT]

    def __reversed__(self):
        end = self._end
        curr = end[PREV]
        while curr is not end:
            yield curr[KEY]
            curr = curr[PREV]

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        return (
            (type(self) is type(other)) and
            (len(self) == len(other)) and
            all(itertools.starmap(operator.eq, zip(self, other)))
        )

    def __clear(self):
        '''Clear the ordered set, removing all items.'''
        self._end = []
        self._end += [None, self._end, self._end]
        self._map = {}


    def __add(self, key, last=True):
        '''
        Add an element to a set.

        This has no effect if the element is already present.

        Specify `last=False` to add the item at the start of the ordered set.
        '''

        if key not in self._map:
            end = self._end
            if last:
                last = end[PREV]
                last[NEXT] = end[PREV] = self._map[key] = [key, last, end]
            else:
                first = end[NEXT]
                first[PREV] = end[NEXT] = self._map[key] = [key, end, first]



class FrozenOrderedSet(BaseOrderedSet):
    '''
    A `frozenset` with an order.

    This behaves like a `frozenset` (i.e. a set that can't be changed after
    creation) except items have an order. (By default they're ordered by
    insertion order, but that order can be changed.)
    '''

    def __hash__(self):
        return hash((type(self), tuple(self)))



class OrderedSet(BaseOrderedSet, collections.abc.MutableSet):
    '''
    A `set` with an order.

    This behaves like a `set` except items have an order. (By default they're
    ordered by insertion order, but that order can be changed.)
    '''

    add = BaseOrderedSet._BaseOrderedSet__add
    clear = BaseOrderedSet._BaseOrderedSet__clear

    def move_to_end(self, key, last=True):
        '''
        Move an existing element to the end (or start if `last=False`.)
        '''
        # Inefficient implementation until someone cares.
        self.remove(key)
        self.add(key, last=last)


    def sort(self, key=None, reverse=False):
        '''
        Sort the items according to their keys, changing the order in-place.

        The optional `key` argument will be passed to the `sorted` function as
        a key function.
        '''
        # Inefficient implementation until someone cares.
        key_function = \
                   comparison_tools.process_key_function_or_attribute_name(key)
        sorted_members = sorted(tuple(self), key=key_function, reverse=reverse)

        self.clear()
        self |= sorted_members


    def discard(self, key):
        '''
        Remove an element from a set if it is a member.

        If the element is not a member, do nothing.
        '''
        if key in self._map:
            key, prev, next = self._map.pop(key)
            prev[NEXT] = next
            next[PREV] = prev

    def pop(self, last=True):
        '''Remove and return an arbitrary set element.'''
        if not self:
            raise KeyError('set is empty')
        key = next(reversed(self) if last else iter(self))
        self.discard(key)
        return key

    def get_frozen(self):
        '''Get a frozen version of this ordered set.'''
        return FrozenOrderedSet(self)



class EmittingOrderedSet(OrderedSet):
    '''An ordered set that emits to `.emitter` every time it's modified.'''

    def __init__(self, iterable=(), *, emitter=None):
        if emitter:
            from python_toolbox.emitting import Emitter
            assert isinstance(emitter, Emitter)
        self.emitter = emitter
        OrderedSet.__init__(self, iterable)

    def add(self, key, last=True):
        '''
        Add an element to a set.

        This has no effect if the element is already present.
        '''
        if key not in self._map:
            super().add(key, last=last)
            self._emit()

    def discard(self, key):
        '''
        Remove an element from a set if it is a member.

        If the element is not a member, do nothing.
        '''
        if key in self._map:
            super().discard(key)
            self._emit()

    def clear(self):
        '''Clear the ordered set, removing all items.'''
        if self:
            super().clear()
            self._emit()

    def set_emitter(self, emitter):
        '''Set `emitter` to be emitted with on every modification.'''
        self.emitter = emitter

    def _emit(self):
        if (self.emitter is not None) and not self._emitter_freezer.frozen:
            self.emitter.emit()

    def move_to_end(self, key, last=True):
        '''
        Move an existing element to the end (or start if `last=False`.)
        '''
        # Inefficient implementation until someone cares.
        with self._emitter_freezer:
            self.remove(key)
        self.add(key, last=last)

    _emitter_freezer = freezing.FreezerProperty()

    def __eq__(self, other):
        return (
            (type(self) is type(other)) and
            (len(self) == len(other)) and
            (self.emitter is other.emitter) and
            all(itertools.starmap(operator.eq, zip(self, other)))
        )

    def get_without_emitter(self):
        '''Get a version of this ordered set without an emitter attached.'''
        return OrderedSet(self)

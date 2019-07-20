# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import operator
import heapq
import itertools
import numbers
import collections
import functools
import copy

from python_toolbox import misc_tools
from python_toolbox import math_tools
from python_toolbox.third_party.decorator import decorator

from .lazy_tuple import LazyTuple
from .ordered_dict import OrderedDict
from .various_ordered_sets import FrozenOrderedSet
from .various_frozen_dicts import FrozenDict, FrozenOrderedDict
from .abstract import Ordered


class _NO_DEFAULT(misc_tools.NonInstantiable):
    '''Stand-in value used in `_BaseBagMixin.pop` when no default is wanted.'''

class _ZeroCountAttempted(Exception):
    '''
    An attempt was made to add a value with a count of zero to a bag.

    This exception is used only internally for flow control; it'll be caught
    internally and the zero item would be silently removed.
    '''

def _count_elements_slow(mapping, iterable):
    '''Put elements from `iterable` into `mapping`.'''
    mapping_get = mapping.get
    for element in iterable:
        mapping[element] = mapping_get(element, 0) + 1

try:
    from _collections import _count_elements
except ImportError:
    _count_elements = _count_elements_slow


def _process_count(count):
    '''Process a count of an item to ensure it's a positive `int`.'''
    if not math_tools.is_integer(count):
        raise TypeError(
            f'You passed {repr(count)} as a count, while a `Bag` can only '
            f'handle integer counts.'
        )
    if count < 0:
        raise TypeError(
            f"You passed {repr(count)} as a count, while `Bag` doesn't support"
            f"negative amounts."
        )

    if count == 0:
        raise _ZeroCountAttempted

    return int(count)


class _BootstrappedCachedProperty(misc_tools.OwnNameDiscoveringDescriptor):
    '''
    A property that is calculated only once for an object, and then cached.

    This is redefined here in `bagging.py`, in addition to having it defined in
    `python_toolbox.caching`, because we can't import the canonical
    `CachedProperty` from there because of an import loop.

    Usage:

        class MyObject:

            # ... Regular definitions here

            def _get_personality(self):
                print('Calculating personality...')
                time.sleep(5) # Time consuming process that creates personality
                return 'Nice person'

            personality = _BootstrappedCachedProperty(_get_personality)

    You can also put in a value as the first argument if you'd like to have it
    returned instead of using a getter. (It can be a tobag static value like
    `0`). If this value happens to be a callable but you'd still like it to be
    used as a static value, use `force_value_not_getter=True`.
    '''
    def __init__(self, getter_or_value, doc=None, name=None,
                 force_value_not_getter=False):
        '''
        Construct the cached property.

        `getter_or_value` may be either a function that takes the parent object
        and returns the value of the property, or the value of the property
        itself, (as long as it's not a callable.)

        You may optionally pass in the name that this property has in the
        class; this will save a bit of processing later.
        '''
        misc_tools.OwnNameDiscoveringDescriptor.__init__(self, name=name)
        if callable(getter_or_value) and not force_value_not_getter:
            self.getter = getter_or_value
        else:
            self.getter = lambda thing: getter_or_value
        self.__doc__ = doc or getattr(self.getter, '__doc__', None)


    def __get__(self, obj, our_type=None):

        if obj is None:
            # We're being accessed from the class itself, not from an object
            return self

        value = self.getter(obj)

        setattr(obj, self.get_our_name(obj, our_type=our_type), value)

        return value


    def __call__(self, method_function):
        '''
        Decorate method to use value of `CachedProperty` as a context manager.
        '''
        def inner(same_method_function, self_obj, *args, **kwargs):
            with getattr(self_obj, self.get_our_name(self_obj)):
                return method_function(self_obj, *args, **kwargs)
        return decorator(inner, method_function)


    def __repr__(self):
        return f'<{type(self).__name__}: {self.our_name or self.getter}>'


class _BaseBagMixin:
    '''
    Mixin for `FrozenBag` and `FrozenOrderedBag`.

    Most of the bag functionality is implemented here, with a few finishing
    touches in the classes that inherit from this. This mixin is used both for
    ordered, unordered, frozen and mutable bags, so only the methods that are
    general to all of them are implemented here.
    '''

    def __init__(self, iterable={}):
        super().__init__()

        if isinstance(iterable, collections.abc.Mapping):
            for key, value, in iterable.items():
                try:
                    self._dict[key] = _process_count(value)
                except _ZeroCountAttempted:
                    continue
        else:
            _count_elements(self._dict, iterable)


    __getitem__ = lambda self, key: self._dict.get(key, 0)

    def most_common(self, n=None):
        '''
        List the `n` most common elements and their counts, sorted.

        Results are sorted from the most common to the least. If `n is None`,
        then list all element counts.

            >>> Bag('abcdeabcdabcaba').most_common(3)
            (('a', 5), ('b', 4), ('c', 3))

        '''
        if n is None:
            return tuple(sorted(self.items(), key=operator.itemgetter(1),
                                reverse=True))
        return tuple(heapq.nlargest(n, self.items(),
                                    key=operator.itemgetter(1)))

    @property
    def elements(self):
        '''
        Iterate over elements repeating each as many times as its count.

            >>> c = Bag('ABCABC')
            >>> tuple(c.elements)
            ('A', 'B', 'A', 'B', 'C', 'C')

        '''
        return itertools.chain.from_iterable(
            itertools.starmap(itertools.repeat, self.items())
        )

    def __contains__(self, item):
        return (self[item] >= 1)

    n_elements = property(
        lambda self: sum(self.values()),
        doc='''Number of total elements in the bag.'''
    )

    @property
    def frozen_bag_bag(self):
        '''
        A `FrozenBagBag` of this bag.

        This means, a bag where `3: 4` means "The original bag has 4 different
        keys with a value of 3."

        Example:

            >>> bag = Bag('abracadabra')
            >>> bag
            Bag({'b': 2, 'r': 2, 'a': 5, 'd': 1, 'c': 1})
            >>> bag.frozen_bag_bag
            FrozenBagBag({1: 2, 2: 2, 5: 1})

        '''
        from .frozen_bag_bag import FrozenBagBag
        return FrozenBagBag(self.values())

    def __or__(self, other):
        '''
        Make a union bag of these two bags.

        The new bag will have, for each key, the higher of the two amounts for
        that key in the two original bags.

        Example:

            >>> Bag('abbb') | Bag('bcc')
            Bag({'b': 3, 'c': 2, 'a': 1})

        '''
        if not isinstance(other, _BaseBagMixin):
            return NotImplemented
        return type(self)(self._dict_type(
            (key, max(self[key], other[key]))
            for key in FrozenOrderedSet(self) | FrozenOrderedSet(other))
        )

    def __and__(self, other):
        '''
        Make an intersection bag of these two bags.

        The new bag will have, for each key, the lower of the two amounts for
        that key in the two original bags.

        Example:

            >>> Bag('abbb') & Bag('bcc')
            Bag({'b': 1,})

        '''
        if not isinstance(other, _BaseBagMixin):
            return NotImplemented
        return type(self)(self._dict_type(
            (key, min(self[key], other[key]))
            for key in FrozenOrderedSet(self) & FrozenOrderedSet(other))
        )


    def __add__(self, other):
        '''
        Make a sum bag of these two bags.

        The new bag will have, for each key, the sum of the two amounts for
        that key in each of the two original bags.

        Example:

            >>> Bag('abbb') + Bag('bcc')
            Bag({'b': 4, 'c': 2, 'a': 1})

        '''
        if not isinstance(other, _BaseBagMixin):
            return NotImplemented
        return type(self)(self._dict_type(
            (key, self[key] + other[key])
            for key in FrozenOrderedSet(self) | FrozenOrderedSet(other))
        )

    def __sub__(self, other):
        '''
        Get the subtraction of one bag from another.

        This creates a new bag which has the items of the first bag minus the
        items of the second one. Negative counts are truncated to zero: If
        there are any items in the second bag that are more than the items in
        the first bag, the result for that key will simply be zero rather than
        a negative amount.
        '''
        if not isinstance(other, _BaseBagMixin):
            return NotImplemented
        return type(self)(self._dict_type(
            (key, max(self[key] - other[key], 0)) for key in self)
        )

    def __mul__(self, other):
        '''Get a new bag that has all counts multiplied by the integer `other`.'''
        if not math_tools.is_integer(other):
            return NotImplemented
        return type(self)(self._dict_type((key, count * other) for
                                          key, count in self.items()))

    __rmul__ = lambda self, other: self * other

    def __floordiv__(self, other):
        '''
        Do a floor-division `self // other`.

        `other` can be either an integer or a bag.

        If `other` is an integer, the result will be the biggest bag possible
        so that `result * other <= self`.

        If `other` is a bag, the result will be the maximum number of times you
        can put `other` inside of `self` without having it surpass `self` for
        any key. (Or in other words, the biggest integer possible so that
        `result * other <= self`.)
        '''

        if math_tools.is_integer(other):
            return (
                type(self)(self._dict_type((key, count // other) for
                                           key, count in self.items()))
            )
        elif isinstance(other, _BaseBagMixin):
            for key in other:
                if key not in self:
                    assert other[key] >= 1
                    return 0
            division_results = []
            for key in self:
                if other[key] >= 1:
                    division_results.append(self[key] // other[key])
            if division_results:
                return min(division_results)
            else:
                raise ZeroDivisionError
        else:
            return NotImplemented

    def __mod__(self, other):
        '''
        Do a modulo `self % other`.

        `other` can be either an integer or a bag.

        If `other` is an integer, the result will be a bag with `% other` done
        on the count of every item from `self`. Or you can also think of it as
        `self - (self // other)`, which happens to be the same bag.

        If `other` is a bag, the result will be the bag that's left when you
        subtract as many copies of `other` from this bag, until you can't
        subtract without truncating some keys. Or in other words, it's `self -
        (self // other)`.
        '''
        if math_tools.is_integer(other):
            return (
                type(self)(self._dict_type((key, count % other) for
                                           key, count in self.items()))
            )
        elif isinstance(other, _BaseBagMixin):
            return divmod(self, other)[1]
        else:
            return NotImplemented

    def __divmod__(self, other):
        '''
        Get `(self // other, self % other)`.

        If `other` is an integer, the first item of the result will be the
        biggest bag possible so that `result * other <= self`. The second item
        will be a bag with `% other` done on the count of every item from
        `self`, or you can also think of it as `self - (self // other)`, which
        happens to be the same bag.

        If `other` is a bag, the first item of the result will be the maximum
        number of times you can put `other` inside of `self` without having it
        surpass `self` for any key. (Or in other words, the biggest integer
        possible so that `result * other <= self`.) The second item will be the
        result of the first item subtracted from `self`.
        '''
        if math_tools.is_integer(other):
            return (
                type(self)(self._dict_type((key, count // other) for
                                           key, count in self.items())),
                type(self)(self._dict_type((key, count % other) for
                                           key, count in self.items())),
            )
        elif isinstance(other, _BaseBagMixin):

            floordiv_result = self // other
            mod_result = type(self)(
                self._dict_type((key, count - other[key] * floordiv_result) for
                                key, count in self.items())
            )
            return (floordiv_result, mod_result)

        else:
            return NotImplemented

    def __pow__(self, other, modulo=None):
        '''Get a new bag with every item raised to the power of `other`.'''
        if not math_tools.is_integer(other):
            return NotImplemented
        if modulo is None:
            return type(self)(self._dict_type((key, count ** other) for
                                              key, count in self.items()))
        else:
            return type(self)(self._dict_type(
                (key, pow(count, other, modulo)) for
                key, count in self.items())
            )

    __bool__ = lambda self: any(True for element in self.elements)

    ###########################################################################
    ### Defining comparison methods: ##########################################
    #                                                                         #
    # We define all the comparison methods manually instead of using
    # `total_ordering` because `total_ordering` assumes that >= means (> and
    # ==) while we, in `FrozenOrderedBag`, don't have that hold because ==
    # takes the items' order into account. Yes, my intelligence and sense of
    # alertness know no bounds.

    def __lt__(self, other):
        '''
        `self` is a strictly smaller bag than `other`.

        That means that for every key in `self`, its count in `other` is bigger
        or equal than in `self`-- And there's at least one key for which the
        count in `other` is strictly bigger.

        Or in other words: `set(self.elements) < set(other.elements)`.
        '''
        if not isinstance(other, _BaseBagMixin):
            return NotImplemented
        found_strict_difference = False # Until challenged.
        all_elements = set(other) | set(self)
        for element in all_elements:
            if self[element] > other[element]:
                return False
            elif self[element] < other[element]:
                found_strict_difference = True
        return found_strict_difference

    def __gt__(self, other):
        '''
        `self` is a strictly bigger bag than `other`.

        That means that for every key in `other`, its count in `other` is smaller
        or equal than in `self`-- And there's at least one key for which the
        count in `other` is strictly smaller.

        Or in other words: `set(self.elements) > set(other.elements)`.
        '''
        if not isinstance(other, _BaseBagMixin):
            return NotImplemented
        found_strict_difference = False # Until challenged.
        all_elements = set(other) | set(self)
        for element in all_elements:
            if self[element] < other[element]:
                return False
            elif self[element] > other[element]:
                found_strict_difference = True
        return found_strict_difference

    def __le__(self, other):
        '''
        `self` is smaller or equal to `other`.

        That means that for every key in `self`, its count in `other` is bigger
        or equal than in `self`.

        Or in other words: `set(self.elements) <= set(other.elements)`.
        '''
        if not isinstance(other, _BaseBagMixin):
            return NotImplemented
        for element, count in self.items():
            if count > other[element]:
                return False
        return True

    def __ge__(self, other):
        '''
        `self` is bigger or equal to `other`.

        That means that for every key in `other`, its count in `other` is bigger
        or equal than in `self`.

        Or in other words: `set(self.elements) >= set(other.elements)`.
        '''
        if not isinstance(other, _BaseBagMixin):
            return NotImplemented
        all_elements = set(other) | set(self)
        for element in all_elements:
            if self[element] < other[element]:
                return False
        return True
    #                                                                         #
    ### Finished defining comparison methods. #################################
    ###########################################################################

    def __repr__(self):
        if not self:
            return f'{type(self).__name__}()'
        return f'{type(self).__name__}({self._dict if self._dict else ""})'

    __deepcopy__ = lambda self, memo: type(self)(
                                               copy.deepcopy(self._dict, memo))

    def __reversed__(self):
        # Gets overridden in `_OrderedBagMixin`.
        raise TypeError("Can't reverse an unordered bag.")


    def get_contained_bags(self):
        '''
        Get all bags that are subsets of this bag.

        This means all bags that have counts identical or smaller for each key.
        '''
        from python_toolbox import combi

        keys, amounts = zip(*((key, amount) for key, amount in self.items()))

        return combi.MapSpace(
            lambda amounts_tuple:
                         type(self)(self._dict_type(zip(keys, amounts_tuple))),
            combi.ProductSpace(map(lambda amount: range(amount+1), amounts))
        )



class _MutableBagMixin(_BaseBagMixin):
    '''Mixin for a bag that's mutable. (i.e. not frozen.)'''

    def __setitem__(self, i, count):
        try:
            super().__setitem__(i, _process_count(count))
        except _ZeroCountAttempted:
            del self[i]


    def setdefault(self, key, default=None):
        '''
        Get value of `key`, unless it's zero/missing, if so set to `default`.
        '''
        current_count = self[key]
        if current_count > 0:
            return current_count
        else:
            self[key] = default
            return default

    def __delitem__(self, key):
        # We're making `__delitem__` not raise an exception on missing or
        # zero-count elements because we're automatically deleting zero-count
        # elements even though they seem to exist from the outside, so we're
        # avoiding raising exceptions where someone would try to explicitly
        # delete them.
        try:
            del self._dict[key]
        except KeyError:
            pass

    def pop(self, key, default=_NO_DEFAULT):
        '''
        Remove `key` from the bag, returning its value.

        If `key` is missing and `default` is given, returns `default`.
        '''
        value = self[key]
        if value == 0 and default is not _NO_DEFAULT:
            return default
        else:
            del self[key]
            return value

    def __ior__(self, other):
        '''
        Make this bag into a union bag of this bag and `other`.

        After the operation, this bag will have, for each key, the higher of
        the two amounts for that key in the two original bags.

            >>> bag = Bag('abbb')
            >>> bag |= Bag('bcc')
            >>> bag
            Bag({'b': 3, 'c': 2, 'a': 1})

        '''
        if not isinstance(other, _BaseBagMixin):
            return NotImplemented
        for key, other_count in tuple(other.items()):
            self[key] = max(self[key], other_count)
        return self


    def __iand__(self, other):
        '''
        Make this bag into an intersection bag of this bag and `other`.

        After the operation, this bag will have, for each key, the lower of the
        two amounts for that key in the two original bags.

            >>> bag = Bag('abbb')
            >>> bag &= Bag('bcc')
            >>> bag
            Bag({'b': 1,})

        '''
        if not isinstance(other, _BaseBagMixin):
            return NotImplemented
        for key, count in tuple(self.items()):
            self[key] = min(count, other[key])
        return self


    def __iadd__(self, other):
        '''
        Make this bag into a sum bag of this bag and `other`.

        After the operation, this bag will have, for each key, the sum of the
        two amounts for that key in each of the two original bags.

        Example:

            >>> bag = Bag('abbb')
            >>> bag += Bag('bcc')
            >>> bag
            Bag({'b': 4, 'c': 2, 'a': 1})

        '''
        if not isinstance(other, _BaseBagMixin):
            return NotImplemented
        for key, other_count in tuple(other.items()):
            self[key] += other_count
        return self


    def __isub__(self, other):
        '''
        Subtract `other` from this bag.

        This reduces the count of each key in this bag by its count in `other`.
        Negative counts are truncated to zero: If there are any items in the
        second bag that are more than the items in the first bag, the result
        for that key will simply be zero rather than a negative amount.
        '''
        if not isinstance(other, _BaseBagMixin):
            return NotImplemented
        for key, other_count in tuple(other.items()):
            self[key] = max(self[key] - other_count, 0)
        return self


    def __imul__(self, other):
        '''Multiply all the counts in this bag by the integer `other`.'''
        if not math_tools.is_integer(other):
            return NotImplemented
        for key in tuple(self):
            self[key] *= other
        return self


    def __ifloordiv__(self, other):
        '''
        Make this bag into a floor-division `self // other`.

        `other` can be either an integer or a bag.

        If `other` is an integer, this bag will have all its counts
        floor-divided by `other`. (You can also think of it as: This bag will
        become the biggest bag possible so that if you multiply it by `other`,
        it'll still be smaller or equal to its old `self`.)

        If `other` is a bag, the result will be the maximum number of times you
        can put `other` inside of `self` without having it surpass `self` for
        any key. (Or in other words, the biggest integer possible so that
        `result * other <= self`.) Since this result is an integer rather than
        a bug, the result variable will be set to it but this bag wouldn't
        really be modified.
        '''
        if not math_tools.is_integer(other):
            return NotImplemented
        for key in tuple(self):
            self[key] //= other
        return self


    def __imod__(self, other):
        '''
        Make this bag int a modulo `self % other`.

        `other` can be either an integer or a bag.

        If `other` is an integer, the result will have all its counts modulo-ed
        by `other`. Or you can also think of it as becoming the bag `self -
        (self // other)`, which happens to be the same bag.

        If `other` is a bag, the result will be the bag that's left when you
        subtract as many copies of `other` from this bag, until you can't
        subtract without truncating some keys. Or in other words, it's `self -
        (self // other)`. Since this result is an integer rather than
        a bug, the result variable will be set to it but this bag wouldn't
        really be modified.
        '''
        if math_tools.is_integer(other):
            for key in tuple(self):
                self[key] %= other
            return self
        elif isinstance(other, _BaseBagMixin):
            floordiv_result = self // other
            self %= floordiv_result
            return self
        else:
            return NotImplemented


    def __ipow__(self, other, modulo=None):
        '''Raise each count in this bag to the power of `other`.'''
        if not math_tools.is_integer(other):
            return NotImplemented
        for key in tuple(self):
            self[key] = pow(self[key], other, modulo)
        return self

    def popitem(self):
        '''
        Pop an item from this bag, returning `(key, count)` and removing it.
        '''
        return self._dict.popitem()

    def get_frozen(self):
        '''Get a frozen version of this bag.'''
        return self._frozen_type(self)


class _OrderedBagMixin(Ordered):
    '''
    Mixin for a bag that's ordered.

    Items will be ordered according to insertion order. In every interface
    where items from this bag are iterated on, they will be returned by their
    order.
    '''
    __reversed__ = lambda self: reversed(self._dict)

    def __eq__(self, other):
        '''
        Is this bag equal to `other`?

        Order *does* count, so if `other` has a different order, the result
        will be `False`.
        '''
        if type(self) != type(other):
            return False
        for item, other_item in itertools.zip_longest(self.items(),
                                                      other.items()):
            if item != other_item:
                return False
        else:
            return True

    index = misc_tools.ProxyProperty(
        '._dict.index',
        doc='Get the index number of a key in the bag.'
    )


class _FrozenBagMixin:
    '''Mixin for a bag that's frozen. (i.e. can't be changed, is hashable.)'''

    # Some properties are redefined here to be cached, since the bag is frozen
    # and they can't change anyway, so why not cache them.

    n_elements = _BootstrappedCachedProperty(
        lambda self: sum(self.values()),
        doc='''Number of total elements in the bag.'''
    )

    @_BootstrappedCachedProperty
    def frozen_bag_bag(self):
        '''
        A `FrozenBagBag` of this bag.

        This means, a bag where `3: 4` means "The original bag has 4 different
        keys with a value of 3."

        Example:

            >>> bag = Bag('abracadabra')
            >>> bag
            Bag({'b': 2, 'r': 2, 'a': 5, 'd': 1, 'c': 1})
            >>> bag.frozen_bag_bag
            FrozenBagBag({1: 2, 2: 2, 5: 1})

        '''
        from .frozen_bag_bag import FrozenBagBag
        return FrozenBagBag(self.values())

    def get_mutable(self):
        '''Get a mutable version of this bag.'''
        return self._mutable_type(self)

    # Poor man's caching done here because we can't import
    # `python_toolbox.caching` due to import loop:
    _contained_bags = None
    def get_contained_bags(self):
        '''
        Get all bags that are subsets of this bag.

        This means all bags that have counts identical or smaller for each key.
        '''
        if self._contained_bags is None:
            self._contained_bags = super().get_contained_bags()
        return self._contained_bags



class _BaseDictDelegator(collections.abc.MutableMapping):
    '''
    Base class for a dict-like object.

    It has its `dict` functionality delegated to `self._dict` which actually
    implements the `dict` functionality. Subclasses override `_dict_type` to
    determine the type of `dict` to use. (Regular or ordered.)
    '''
    def __init__(self, dict=None, **kwargs):
        self._dict = self._dict_type()
        if dict is not None:
            self.update(dict)
        if len(kwargs):
            self.update(kwargs)
    def __len__(self): return len(self._dict)
    def __getitem__(self, key):
        if key in self._dict:
            return self._dict[key]
        if hasattr(self.__class__, '__missing__'):
            return self.__class__.__missing__(self, key)
        raise KeyError(key)
    def __setitem__(self, key, item): self._dict[key] = item
    def __delitem__(self, key): del self._dict[key]
    def __iter__(self):
        return iter(self._dict)

    def __contains__(self, key):
        return key in self._dict

    def __repr__(self): return repr(self._dict)
    def copy(self):
        if self.__class__ is _OrderedDictDelegator:
            return _OrderedDictDelegator(self._dict.copy())
        import copy
        data = self._dict
        try:
            self._dict = self._dict_type()
            c = copy.copy(self)
        finally:
            self._dict = data
        c.update(self)
        return c
    @classmethod
    def fromkeys(cls, iterable, value=None):
        d = cls()
        for key in iterable:
            d[key] = value
        return d

class _OrderedDictDelegator(Ordered, _BaseDictDelegator):
    '''
    An `OrderedDict`-like object.

    It has its `OrderedDict` functionality delegated to `self._dict` which is
    an actual `OrderedDict`.
    '''
    _dict_type = OrderedDict
    index = misc_tools.ProxyProperty(
        '._dict.index',
        doc='Get the index number of a key in this dict.'
    )
    move_to_end = misc_tools.ProxyProperty(
        '._dict.move_to_end',
        doc='Move a key to the end (or start by passing `last=False`.)'
    )
    sort = misc_tools.ProxyProperty(
        '._dict.sort',
        doc='Sort the keys in this dict. (With optional `key` function.)'
    )

class _DictDelegator(_BaseDictDelegator):
    '''
    A `dict`-like object.

    It has its `dict` functionality delegated to `self._dict` which is an
    actual `dict`.
    '''

    _dict_type = dict


class Bag(_MutableBagMixin, _DictDelegator):
    '''
    A bag that counts items.

    This is a mapping between items and their count:

        >>> Bag('aaabcbc')
        Bag({'a': 3, 'b': 2, 'c': 2})

    It can be created from either an iterable like above, or from a `dict`.

    This class provides a lot of methods that `collections.Counter` doesn't;
    among them are a plethora of arithmetic operations (both between bags and
    bags and between bags and integers), comparison methods between bags, and
    more. This class is also more restricted than `collections.Counter`; only
    positive integers may be used as counts (zeros are weeded out), so we don't
    need to deal with all the complications of non-numerical counts.
    '''



class OrderedBag(_OrderedBagMixin, _MutableBagMixin, _OrderedDictDelegator):
    '''
    An ordered bag that counts items.

    This is a ordered mapping between items and their count:

        >>> OrderedBag('aaabcbc')
        OrderedBag((('a', 3), ('b', 2), ('c', 2)))

    It can be created from either an iterable like above, or from a `dict`.

    This class provides a lot of methods that `collections.Counter` doesn't;
    among them are a plethora of arithmetic operations (both between bags and
    bags and between bags and integers), comparison methods between bags, and
    more. This class is also more restricted than `collections.Counter`; only
    positive integers may be used as counts (zeros are weeded out), so we don't
    need to deal with all the complications of non-numerical counts.

    Also, unlike `collections.Counter`, items are ordered by insertion order.
    (Simliarly to `collections.OrderedDict`.)
    '''
    def popitem(self, last=True):
        '''
        Pop an item from this bag, returning `(key, count)` and removing it.

        By default, the item will be popped from the end. Pass `last=False` to
        pop from the start.
        '''
        return self._dict.popitem(last=last)
    move_to_end = misc_tools.ProxyProperty(
        '._dict.move_to_end',
        doc='Move a key to the end (or start by passing `last=False`.)'
    )
    sort = misc_tools.ProxyProperty(
        '._dict.sort',
        doc='Sort the keys in this bag. (With optional `key` function.)'
    )

    @property
    def reversed(self):
        '''Get a version of this `OrderedBag` with key order reversed.'''
        return type(self)(self._dict_type(reversed(tuple(self.items()))))


class FrozenBag(_BaseBagMixin, _FrozenBagMixin, FrozenDict):
    '''
    An immutable bag that counts items.

    This is an immutable mapping between items and their count:

        >>> FrozenBag('aaabcbc')
        FrozenBag({'a': 3, 'b': 2, 'c': 2})

    It can be created from either an iterable like above, or from a `dict`.

    This class provides a lot of methods that `collections.Counter` doesn't;
    among them are a plethora of arithmetic operations (both between bags and
    bags and between bags and integers), comparison methods between bags, and
    more. This class is also more restricted than `collections.Counter`; only
    positive integers may be used as counts (zeros are weeded out), so we don't
    need to deal with all the complications of non-numerical counts.

    Also, unlike `collections.Counter`, it's immutable, therefore it's also
    hashable, and thus it can be used as a key in dicts and sets.
    '''
    def __hash__(self):
        return hash((type(self), frozenset(self.items())))


class FrozenOrderedBag(_OrderedBagMixin, _FrozenBagMixin, _BaseBagMixin,
                       FrozenOrderedDict):
    '''
    An immutable, ordered bag that counts items.

    This is an ordered mapping between items and their count:

        >>> FrozenOrderedBag('aaabcbc')
        FrozenOrderedBag((('a', 3), ('b', 2), ('c', 2)))

    It can be created from either an iterable like above, or from a `dict`.

    This class provides a lot of methods that `collections.Counter` doesn't;
    among them are a plethora of arithmetic operations (both between bags and
    bags and between bags and integers), comparison methods between bags, and
    more. This class is also more restricted than `collections.Counter`; only
    positive integers may be used as counts (zeros are weeded out), so we don't
    need to deal with all the complications of non-numerical counts.

    Also, unlike `collections.Counter`:

     -  Items are ordered by insertion order. (Simliarly to
        `collections.OrderedDict`.)

     - It's immutable, therefore it's also hashable, and thus it can be used as
       a key in dicts and sets.

    '''
    def __hash__(self):
        return hash((type(self), tuple(self.items())))

    @_BootstrappedCachedProperty
    def reversed(self):
        '''Get a version of this `FrozenOrderedBag` with key order reversed.'''
        return type(self)(self._dict_type(reversed(tuple(self.items()))))



Bag._frozen_type = FrozenBag
OrderedBag._frozen_type = FrozenOrderedBag
FrozenBag._mutable_type = Bag
FrozenOrderedBag._mutable_type = OrderedBag

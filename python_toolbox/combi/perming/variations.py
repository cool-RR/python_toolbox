# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import exceptions
from python_toolbox import cute_iter_tools
from python_toolbox import nifty_collections
from python_toolbox import caching
from python_toolbox.third_party import sortedcontainers

from ..selection_space import SelectionSpace


class Variation(nifty_collections.CuteEnum):
    '''
    A variation that a `PermSpace` might have.

    The `combi` package allows many different variations on `PermSpace`. It may
    be range-applied, recurrent, partial, a combination, and more. Each of
    these is a `Variation` object. This `Variation` object is used mostly for
    meta purposes.
    '''
    RAPPLIED = 'rapplied'
    RECURRENT = 'recurrent'
    PARTIAL = 'partial'
    COMBINATION = 'combination'
    DAPPLIED = 'dapplied'
    FIXED = 'fixed'
    DEGREED = 'degreed'
    SLICED = 'sliced'
    TYPED = 'typed'



class UnallowedVariationSelectionException(exceptions.CuteException):
    '''
    An unallowed selection of variations was attempted.

    For example, you can't make dapplied combination spaces, and if you'll try,
    you'll get an earful of this here exception.
    '''
    def __init__(self, variation_clash):
        self.variation_clash = variation_clash
        assert variation_clash in variation_clashes
        super().__init__(
            "You can't create a `PermSpace` that's %s." % (
                ' and '.join(
                    '%s%s' % (
                        '' if included else 'not ',
                        variation.value
                    ) for variation, included in variation_clash.items()
                )
            )
        )


variation_clashes = (
    {Variation.DAPPLIED: True, Variation.COMBINATION: True,},
    {Variation.DEGREED: True, Variation.COMBINATION: True,},
    {Variation.DEGREED: True, Variation.PARTIAL: True,},
    {Variation.DEGREED: True, Variation.RECURRENT: True,},
    {Variation.COMBINATION: True, Variation.FIXED: True,},
    {Variation.RAPPLIED: False, Variation.RECURRENT: True,},
)
'''Variations that can't be used with each other.'''


class VariationSelectionSpace(SelectionSpace):
    '''
    The space of all variation selections.

    Every member in this space is a `VariationSelection`, meaning a bunch of
    variations that a `PermSpace` might have (like whether it's rapplied, or
    sliced, or a combination). This is the space of all possible
    `VariationSelection`s, both the allowed ones and the unallowed ones.
    '''
    def __init__(self):
        SelectionSpace.__init__(self, Variation)

    @caching.cache()
    def __getitem__(self, i):
        return VariationSelection(SelectionSpace.__getitem__(self, i))

    def index(self, variation_selection):
        return super().index(variation_selection.variations)

    @caching.cache()
    def __repr__(self):
        return '<VariationSelectionSpace>'

    @caching.CachedProperty
    def allowed_variation_selections(self):
        '''
        A tuple of all `VariationSelection` objects that are allowed.

        This means all variation selections which can be used in a `PermSpace`.
        '''
        return tuple(variation_selection for variation_selection in self if
                     variation_selection.is_allowed)

    @caching.CachedProperty
    def unallowed_variation_selections(self):
        '''
        A tuple of all `VariationSelection` objects that are unallowed.

        This means all variation selections which cannot be used in a
        `PermSpace`.
        '''
        return tuple(variation_selection for variation_selection in self if
                     not variation_selection.is_allowed)


variation_selection_space = VariationSelectionSpace()


class VariationSelectionType(type):
    __call__ = lambda cls, variations: cls._create_from_sorted_set(
                                        sortedcontainers.SortedSet(variations))

class VariationSelection(metaclass=VariationSelectionType):
    '''
    A selection of variations of a `PermSpace`.

    The `combi` package allows many different variations on `PermSpace`. It may
    be range-applied, recurrent, partial, a combination, and more. Any
    selection of variations from this list is represented by a
    `VariationSelection` object. Some are allowed, while others aren't allowed.
    (For example a `PermSpace` that is both dapplied and a combination is not
    allowed.)

    This type is cached, meaning that after you create one from an iterable of
    variations and then try to create an identical one by using an iterable
    with the same variations, you'll get the original `VariationSelection`
    object you created.
    '''
    @classmethod
    @caching.cache()
    def _create_from_sorted_set(cls, variations):
        '''Create a `VariationSelection` from a `SortedSet` of variations.'''
        # This method exsits so we could cache canonically. The `__new__`
        # method canonicalizes the `variations` argument to a `SortedSet` and
        # we cache according to it.
        variation_selection = super().__new__(cls)
        variation_selection.__init__(variations)
        return variation_selection

    def __init__(self, variations):
        self.variations = variations
        assert cute_iter_tools.is_sorted(self.variations)
        self.is_rapplied = Variation.RAPPLIED in self.variations
        self.is_recurrent = Variation.RECURRENT in self.variations
        self.is_partial = Variation.PARTIAL in self.variations
        self.is_combination = Variation.COMBINATION in self.variations
        self.is_dapplied = Variation.DAPPLIED in self.variations
        self.is_fixed = Variation.FIXED in self.variations
        self.is_degreed = Variation.DEGREED in self.variations
        self.is_sliced = Variation.SLICED in self.variations
        self.is_typed = Variation.TYPED in self.variations
        self.is_pure = not self.variations

    @caching.cache()
    def __repr__(self):
        return '<%s #%s: %s>' % (
            type(self).__name__,
            self.number,
            ', '.join(variation.value for variation in self.variations)
                                                                      or 'pure'
        )

    @caching.CachedProperty
    def is_allowed(self):
        '''Is this `VariationSelection` allowed to be used in a `PermSpace`?'''
        _variations_set = set(self.variations)
        for variation_clash in variation_clashes:
            for variation, included in variation_clash.items():
                if (variation in _variations_set) != included:
                    break
            else:
                return False
        else:
            return True

    number = caching.CachedProperty(
        variation_selection_space.index,
        '''Serial number in the space of all variation selections.'''
    )

    _reduced = caching.CachedProperty(lambda self: (type(self), self.number))
    _hash = caching.CachedProperty(lambda self: hash(self._reduced))
    __eq__ = lambda self, other: isinstance(other, VariationSelection) and \
                                                self._reduced == other._reduced
    __hash__ = lambda self: self._hash


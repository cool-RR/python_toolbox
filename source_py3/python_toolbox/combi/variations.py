from python_toolbox import exceptions
from python_toolbox import cute_iter_tools
from python_toolbox import nifty_collections
from python_toolbox import caching
from python_toolbox.third_party import sortedcontainers

from .selection_space import SelectionSpace


class UnallowedVariationSelectionException(exceptions.CuteException):
    '''
    
    blocktodo use everywhere
    let it take variations
    make variation classes mostly for this and testing'''
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
        

class Variation(nifty_collections.CuteEnum):
    RAPPLIED = 'rapplied'
    RECURRENT = 'recurrent'
    PARTIAL = 'partial'
    COMBINATION = 'combination'
    DAPPLIED = 'dapplied'
    FIXED = 'fixed'
    DEGREED = 'degreed'
    SLICED = 'sliced'
    
        
variation_clashes = (
    {Variation.DAPPLIED: True, Variation.COMBINATION: True,},
    {Variation.DEGREED: True, Variation.COMBINATION: True,},
    {Variation.DEGREED: True, Variation.PARTIAL: True,},
    {Variation.DEGREED: True, Variation.RECURRENT: True,},
    {Variation.COMBINATION: True, Variation.FIXED: True,},
    {Variation.RAPPLIED: False, Variation.RECURRENT: True,},
)


class VariationSelectionSpace(SelectionSpace):
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
    
variation_selection_space = VariationSelectionSpace()

        
class VariationSelectionType(type):
    __call__ = lambda cls, variations: cls._create_from_tuple(
                                   cls, sortedcontainers.SortedSet(variations))
    
class VariationSelection(metaclass=VariationSelectionType):
    @caching.cache()
    def _create_from_tuple(cls, variations):
        # This method exsits so we could cache canonically. The `__new__`
        # method canonicalizes the `variations` argument and we cache according
        # to it.
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
        _variations_set = set(self.variations)
        for variation_clash in variation_clashes:
            for variation, included in variation_clash.items():
                if (variation in _variations_set) != included:
                    break
            else:
                return False
        else:
            return True
        
    number = caching.CachedProperty(variation_selection_space.index)
    
    _reduced = caching.CachedProperty(lambda self: (type(self), self.number))
    _hash = caching.CachedProperty(lambda self: hash(self._reduced))
    __eq__ = lambda self, other: isinstance(other, VariationSelection) and \
                                                self._reduced == other._reduced
    __hash__ = lambda self: self._hash
        
     
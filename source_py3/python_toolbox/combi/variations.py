from python_toolbox import cute_iter_tools
from python_toolbox import nifty_collections
from python_toolbox import caching
from python_toolbox.third_party import sortedcontainers

from .selection_space import SelectionSpace


class UnsupportedVariationCombinationException(Exception):
    '''blocktodo use everywhere
    let it take variations
    make variation classes mostly for this and testing'''
    

class PermSpaceVariation(nifty_collections.CuteEnum):
    RAPPLIED = 'rapplied'
    RECURRENT = 'recurrent'
    PARTIAL = 'partial'
    COMBINATION = 'combination'
    DAPPLIED = 'dapplied'
    FIXED = 'fixed'
    DEGREED = 'degreed'
    SLICED = 'sliced'
    
        
variation_clashes = (
    {PermSpaceVariation.DEGREED, PermSpaceVariation.COMBINATION},
    {PermSpaceVariation.DEGREED, PermSpaceVariation.PARTIAL},
    {PermSpaceVariation.DEGREED, PermSpaceVariation.RECURRENT},
    {PermSpaceVariation.COMBINATION, PermSpaceVariation.FIXED},
)


class VariationSelectionSpace(SelectionSpace):
    def __init__(self):
        SelectionSpace.__init__(self, PermSpaceVariation)
        
    @caching.cache()
    def __getitem__(self, i):
        return VariationSelection(SelectionSpace.__getitem__(self, i))
        
    @caching.cache()
    def __repr__(self):
        return '<VariationSelectionSpace>'
    
        
class VariationSelection():
    __new__ = lambda cls, variations: cls._create_from_tuple(
        tuple(sorted(set(variations)))
    )
    _create_from_tuple = caching.cache()(lambda self: super().__new__(variations))
    # This method exsits so we could cache canonically. The `__new__` method
    # canonicalizes the `variations` argument and we cache according to it.
        
    def __init__(self, variations):
        self.variations = variations
        
    @caching.cache()
    def __repr__(self):
        return '<%s: %s>' % (
            type(self).__name__,
            ', '.join(variation.value for variation in
                      sorted(self.variations, key=PermSpaceVariation.index))
        )
    
    @caching.CachedProperty
    def is_allowed(self):
        return not any(variation_clash <= self.variations for
                       variation_clash in variation_clashes)
    
     
variation_selection_space = VariationSelectionSpace()
variation_selection_space[7].is_allowed
repr(variation_selection_space[7])
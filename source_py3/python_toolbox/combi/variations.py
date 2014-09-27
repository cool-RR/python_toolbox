import enum

from python_toolbox import cute_iter_tools
from python_toolbox import caching

from .selection_space import SelectionSpace


class UnsupportedVariationCombinationException(Exception):
    '''blocktodo use everywhere
    let it take variations
    make variation classes mostly for this and testing'''
    

class PermSpaceVariation(enum.Enum):
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


allowed_variation_combinations, unallowed_variation_combinations = \
                                                 cute_iter_tools.double_filter(
    lambda variation_combination: any(
                variation_clash <= variation_combination for variation_clash in
                                                            variation_clashes),
    SelectionSpace(PermSpaceVariation),
    lazy_tuple=True
)



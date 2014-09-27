# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

import pickle
import itertools
import collections

from python_toolbox import sequence_tools

from python_toolbox import combi
from python_toolbox.combi import *

infinity = float('inf')
infinities = (infinity, -infinity)


def _check_variation_selection(variation_selection):
    assert isinstance(variation_selection, combi.variations.VariationSelection)
    
    kwargs = {}
    
    iterable_or_length = (
        'abracadabra' if variation_selection.is_recurrent else
        tuple(range(100, -10, -10)) if variation_selection.is_rapplied else 11
    )
    kwargs['iterable_or_length'] = iterable_or_length
    iterable = (iterable_or_length if
                isinstance(iterable_or_length, collections.Iterable) else
                sequence_tools.CuteRange(iterable_or_length))
    
    if variation_selection.is_dapplied:
        domain = 'switzerland'
        kwargs['domain'] = domain
    else:
        domain = sequence_tools.CuteRange(11)
        
    if variation_selection.is_partial:
        fixed_map = {domain[1]: range[1], domain[5]: range[4],}
    else:
        n_elements = (5 if )
        
    perm_space = PermSpace(
        **kwargs
    )
    
    
    
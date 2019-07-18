# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import pickle
import itertools

from python_toolbox import cute_iter_tools
from python_toolbox import sequence_tools

from python_toolbox import combi
from python_toolbox.combi import *

infinity = float('inf')
infinities = (infinity, -infinity)


def test():
    assert len(combi.perming.variations.variation_selection_space) == \
                                   2 ** len(combi.perming.variations.Variation)

    for i, variation_selection in \
                 enumerate(combi.perming.variations.variation_selection_space):
        assert isinstance(variation_selection,
                          combi.perming.variations.VariationSelection)
        assert combi.perming.variations.variation_selection_space. \
                                                index(variation_selection) == i
        assert cute_iter_tools.is_sorted(variation_selection.variations)

        assert isinstance(variation_selection.is_allowed, bool)



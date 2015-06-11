# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''A package for doing a binary search in a sequence.'''

from .roundings import (Rounding, LOW, LOW_IF_BOTH, LOW_OTHERWISE_HIGH, HIGH,
                        HIGH_IF_BOTH, HIGH_OTHERWISE_LOW, EXACT, CLOSEST,
                        CLOSEST_IF_BOTH, BOTH)
from .functions import (binary_search, binary_search_by_index,
                        make_both_data_into_preferred_rounding)
from .binary_search_profile import BinarySearchProfile
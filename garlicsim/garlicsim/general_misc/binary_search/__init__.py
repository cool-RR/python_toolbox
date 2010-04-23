# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''A package for doing a binary search in a sequence.'''

from .roundings import Rounding, LOW, HIGH, EXACT, CLOSEST, BOTH
from .functions import (binary_search, binary_search_by_index,
                        make_both_data_into_preferred_rounding)
# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

import threading
import collections
import itertools

from python_toolbox import decorator_tools
from python_toolbox import comparison_tools

infinity = float('inf')


@comparison_tools.total_ordering    
class IntegerSet(collections.Set):
    def __init__(self, iterable):
        self.integers = 
        

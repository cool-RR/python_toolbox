# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

import itertools
import types

from python_toolbox import nifty_collections

from python_toolbox.cute_iter_tools import fill



def test():
    assert fill(range(4), fill_value='Meow', length=7, sequence_type=list) == [
        0, 1, 2, 3, 'Meow', 'Meow', 'Meow'
    ]
    assert isinstance(fill(range(4), fill_value='Meow'), types.GeneratorType)
    
    assert fill(range(4), fill_value_maker=iter(range(10)).next, length=7,
                sequence_type=tuple) == (0, 1, 2, 3, 0, 1, 2)
    
    lazy_tuple = fill(range(4), fill_value='Meow', length=7, lazy_tuple=True)
    
    assert isinstance(lazy_tuple, nifty_collections.LazyTuple)
    assert not lazy_tuple.collected_data
    
    assert lazy_tuple == (0, 1, 2, 3, 'Meow', 'Meow', 'Meow')
                                                            
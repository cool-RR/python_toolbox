# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

import itertools
import types

from python_toolbox.cute_iter_tools import fill



def test():
    assert fill(range(4), fill_value='Meow', length=7, sequence_type=list) == [
        0, 1, 2, 3, 'Meow', 'Meow', 'Meow'
    ]
    assert isinstance(fill(range(4), fill_value='Meow'), types.GeneratorType)
    
    assert fill(range(4), fill_value_maker=iter(range(10)).next, length=7,
                sequence_type=tuple) == (0, 1, 2, 3, 0, 1, 2)
    
                                                            
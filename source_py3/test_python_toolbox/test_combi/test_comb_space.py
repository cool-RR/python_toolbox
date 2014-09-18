# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox.combi import *


def test():
    comb_space = CombSpace('dumber', 2)
    assert isinstance(comb_space, CombSpace)
    assert isinstance(comb_space, PermSpace)
    assert comb_space.length == 1 + 2 + 3 + 4 + 5
    things_in_comb_space = (
        'du', 'db', 'br', ('d', 'u'), {'d', 'u'}, Comb('du', comb_space)
    )
    things_not_in_comb_space = (
        'dx', 'dub', ('d', 'x'), {'d', 'u', 'b'}, Comb('dux', comb_space),
        Comb('du', CombSpace('other', 2))
    )
    
    for thing in things_in_comb_space:
        assert thing in comb_space
    for thing in things_not_in_comb_space:
        assert thing not in comb_space
    
    
    
    
    
    
    

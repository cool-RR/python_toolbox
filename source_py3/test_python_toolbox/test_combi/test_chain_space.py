# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox.combi import *


def test_chain_spaces():
    chain_space = ChainSpace((range(3), 'meow', range(2, -1, -1)))
    assert tuple(chain_space) == (0, 1, 2, 'm', 'e', 'o', 'w', 2, 1, 0)
    assert len(chain_space) == chain_space.length == 10
    assert bool(chain_space) is True
    for i, item in enumerate(chain_space):
        assert chain_space[i] == item
        assert chain_space.index(item) == i
        
    assert chain_space == chain_space
    
    assert 0 in chain_space
    assert 'm' in chain_space
    assert [] not in chain_space
    
    assert not ChainSpace(())
    


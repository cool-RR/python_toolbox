# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import cute_testing

from python_toolbox.combi import *


def test_chain_spaces():
    chain_space = ChainSpace((range(3), 'meow', range(22, 19, -1)))
    assert tuple(chain_space) == (0, 1, 2, 'm', 'e', 'o', 'w', 22, 21, 20)
    assert len(chain_space) == chain_space.length == 10
    assert bool(chain_space) is True
    for i, item in enumerate(chain_space):
        assert chain_space[i] == item
        assert chain_space.index(item) == i
        
    assert chain_space == chain_space
    
    assert 0 in chain_space
    assert 'm' in chain_space
    assert [] not in chain_space
    
    with cute_testing.RaiseAssertor(ValueError): chain_space.index('nope')
    with cute_testing.RaiseAssertor(IndexError): chain_space[-11]
    with cute_testing.RaiseAssertor(IndexError): chain_space[-110]
    with cute_testing.RaiseAssertor(IndexError): chain_space[11]
    with cute_testing.RaiseAssertor(IndexError): chain_space[1100]
    
    assert chain_space[-1] == 20
    assert chain_space[-2] == 21
    assert chain_space[-10] == 0
    
    assert not ChainSpace(())
    


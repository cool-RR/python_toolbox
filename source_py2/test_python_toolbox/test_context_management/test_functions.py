# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import context_management

from python_toolbox import freezing


def test_nested():
    freezer_a = freezing.Freezer()
    freezer_b = freezing.Freezer()
    freezer_c = freezing.Freezer()
    freezer_d = freezing.Freezer()
    
    freezers = (freezer_a, freezer_b, freezer_c)
    
    assert freezer_a.frozen == freezer_b.frozen == freezer_c.frozen == \
                                                          freezer_d.frozen == 0
    
    with context_management.nested(*freezers):
        assert freezer_a.frozen == freezer_b.frozen == freezer_c.frozen == 1
        assert freezer_d.frozen == 0
        
    assert freezer_a.frozen == freezer_b.frozen == freezer_c.frozen == \
               freezer_d.frozen == 0
    
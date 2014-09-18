# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox.combi import *


def test():
    selection_space = SelectionSpace(range(5))
    assert len(tuple(selection_space)) == len(selection_space) == 2 ** 5
    assert selection_space[0] == ()
    assert selection_space[-1] == tuple(range(5))
    
    
# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

import pickle
import itertools

from python_toolbox import sequence_tools

from python_toolbox import combi
from python_toolbox.combi import *

infinity = float('inf')
infinities = (infinity, -infinity)


def test_perm_spaces():
    pure_0a = PermSpace(4)
    pure_0b = PermSpace(range(4))
    pure_0c = PermSpace(list(range(4)))
    pure_0d = PermSpace(iter(range(4)))

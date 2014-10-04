from python_toolbox import math_tools
from python_toolbox import caching

from .perm import Perm
from .comb_space import CombSpace

        
class Comb(Perm):
    def __init__(self, perm_sequence, perm_space):
        assert isinstance(perm_space, CombSpace)
        Perm.__init__(self, perm_sequence=perm_sequence,
                      perm_space=perm_space)
        


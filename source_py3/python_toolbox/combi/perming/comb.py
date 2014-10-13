from .perm import Perm, UnrecurrentedPerm
from .comb_space import CombSpace

        
class Comb(Perm):
    '''blocktododoc'''
    def __init__(self, perm_sequence, perm_space=None):
        # Unlike for `Perm`, we must have a `perm_space` in the arguments. It
        # can either be in the `perm_space` argument, or if the `perm_sequence`
        # we got is a `Comb`, then we'll take the one from it.
        assert isinstance(perm_space, CombSpace) or \
                                                isinstance(perm_sequence, Comb)
        
        Perm.__init__(self, perm_sequence=perm_sequence,
                      perm_space=perm_space)
        

class UnrecurrentedComb(UnrecurrentedPerm, Comb):
    pass
        
        
        


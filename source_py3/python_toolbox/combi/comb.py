from python_toolbox import math_tools
from python_toolbox import caching

from .perm import Perm
from .comb_space import CombSpace

        
class Comb(Perm):
    def __init__(self, number_or_perm_sequence, perm_space):
        assert isinstance(perm_space, CombSpace)
        Perm.__init__(self, number_or_perm_sequence=number_or_perm_sequence,
                      perm_space=perm_space)
        
    @caching.CachedProperty
    def _perm_sequence(self):
        comb_space = self.just_dapplied_rapplied_perm_space.combinationed
        assert (0 <= self.number < comb_space.length)
        wip_number = (comb_space.length - 1 - self.number)
        wip_perm_sequence = []
        for i in range(comb_space.n_elements, 0, -1):
            for j in range(comb_space.sequence_length, i - 2, -1):
                candidate = math_tools.binomial(j, i)
                if candidate <= wip_number:
                    wip_perm_sequence.append(
                        comb_space.sequence[-(j+1)]
                    )
                    wip_number -= candidate
                    break
            else:
                raise RuntimeError
        result = tuple(wip_perm_sequence)
        assert len(result) == self.length
        return result
      

    @caching.CachedProperty
    def number(self):
        '''
        
        The number here is not necessarily the number with which the perm was
        fetched from the perm space; it's the number of the perm in a perm
        space that is neither degreed, fixed or sliced.
        '''
        if self.is_rapplied or self.is_dapplied:
            return self.unrapplied.undapplied.number
        
        processed_perm_sequence = tuple(
            self.just_dapplied_rapplied_perm_space.sequence_length - 1 -
            item for item in self._perm_sequence[::-1]
        )
        return self.just_dapplied_rapplied_perm_space.length - 1 - sum(
            (math_tools.binomial(item, i) for i, item in
                                  enumerate(processed_perm_sequence, start=1)),
            0
        )
    

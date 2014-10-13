

from .perm_space import PermSpace

class CombSpace(PermSpace):
    '''
    A space of combinations.
    
    
    
    Every item in a `CombSpace` is a `Comb`.
    '''
    def __init__(self, iterable_or_length, n_elements, *, slice_=None,
                 perm_type=None, _domain_for_checking=None,
                 _degrees_for_checking=None):
        PermSpace.__init__(
            self, iterable_or_length=iterable_or_length, n_elements=n_elements,
            is_combination=True, slice_=slice_, perm_type=perm_type,
            domain=_domain_for_checking, degrees=_degrees_for_checking
        )
        
        
    def __repr__(self):
        sequence_repr = repr(self.sequence)
        if len(sequence_repr) > 40:
            sequence_repr = \
                      ''.join((sequence_repr[:35], ' ... ', sequence_repr[-1]))
            
        return '<%s: %s%s>%s' % (
            type(self).__name__,
            sequence_repr,
            (', n_elements=%s' % (self.n_elements,)) if self.is_partial
                                                                       else '',
            ('[%s:%s]' % (self.slice_.start, self.slice_.stop)) if
                                                         self.is_sliced else ''
        )
        


from .comb import Comb

# Must set this after-the-fact because of import loop:
CombSpace.perm_type = CombSpace._default_perm_type = Comb

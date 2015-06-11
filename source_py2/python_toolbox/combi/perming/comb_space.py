# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import misc_tools

from .perm_space import PermSpace


class CombSpace(PermSpace):
    '''
    A space of combinations.
    
    This is a subclass of `PermSpace`; see its documentation for more details.
    
    Each item in a `CombSpace` is a `Comb`, i.e. a combination. This is similar
    to `itertools.combinations`, except it offers far, far more functionality.
    The combinations may be accessed by index number, the combinations can be
    of a custom type, the space may be sliced, etc.
    
    Here is the simplest possible `CombSpace`:
    
        >>> comb_space = CombSpace(4, 2)
        <CombSpace: 0..3, n_elements=2>
        >>> comb_space[2]
        <Comb, n_elements=2: (0, 3)>
        >>> tuple(comb_space)
        (<Comb, n_elements=2: (0, 1)>, <Comb, n_elements=2: (0, 2)>,
         <Comb, n_elements=2: (0, 3)>, <Comb, n_elements=2: (1, 2)>,
         <Comb, n_elements=2: (1, 3)>, <Comb, n_elements=2: (2, 3)>)

    The members are `Comb` objects, which are sequence-like objects that have
    extra functionality. (See documentation of `Comb` and `Perm` for more
    info.)
    '''
    @misc_tools.limit_positional_arguments(3)
    def __init__(self, iterable_or_length, n_elements, slice_=None,
                 perm_type=None, _domain_for_checking=None,
                 _degrees_for_checking=None):
        PermSpace.__init__(
            self, iterable_or_length=iterable_or_length, n_elements=n_elements,
            is_combination=True, slice_=slice_, perm_type=perm_type,
            domain=_domain_for_checking, degrees=_degrees_for_checking
        )
        
        
    def __repr__(self):
        sequence_repr = self.sequence.short_repr if \
                  hasattr(self.sequence, 'short_repr') else repr(self.sequence)
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
CombSpace.perm_type = CombSpace.default_perm_type = Comb

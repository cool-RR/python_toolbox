import itertools

from python_toolbox import nifty_collections


###############################################################################

_length_of_recurrent_perm_space_cache = {}

def calculate_length_of_recurrent_perm_space(k, fbb):
    '''blocktododoc'''
    cache = _length_of_recurrent_perm_space_cache
    if not isinstance(fbb, nifty_collections.FrozenBagBag):
        fbb = nifty_collections.FrozenBagBag(fbb)
    if k == 0:
        return 1
    elif k == 1:
        assert fbb
        # (Works because `FrozenBagBag` has a functioning `__bool__`,
        # unlike Python's `Counter`.)
        return fbb.n_elements
    try:
        return cache[(k, fbb)]
    except KeyError:
        pass
    
    levels = []
    current_fbbs = {fbb}
    while len(levels) < k and current_fbbs:
        k_ = k - len(levels)
        levels.append(
            {fbb_: fbb_.get_sub_fbbs_for_one_crate_removed()
             for fbb_ in current_fbbs
                          if (k_, fbb_) not in cache}
        )
        current_fbbs = set(itertools.chain(*levels[-1].values()))
        
    # The last level is calculated. Time to make our way up.
    for k_, level in enumerate(reversed(levels), (k - len(levels) + 1)):
        if k_ == 1:
            for fbb_, sub_fbb_bag in level.items():
                cache[(k_, fbb_)] = fbb_.n_elements
        else:
            for fbb_, sub_fbb_bag in level.items():
                cache[(k_, fbb_)] = sum(
                    (cache[(k_ - 1, sub_fbb)] * factor for
                           sub_fbb, factor in sub_fbb_bag.items())
                )
    
    return cache[(k, fbb)]
        
    


###############################################################################

_length_of_recurrent_comb_space_cache = {}

def calculate_length_of_recurrent_comb_space(k, fbb):
    '''blocktododoc'''
    cache = _length_of_recurrent_comb_space_cache
    if not isinstance(fbb, nifty_collections.FrozenBagBag):
        fbb = nifty_collections.FrozenBagBag(fbb)
    if k == 0:
        return 1
    elif k == 1:
        assert fbb
        # (Works because `FrozenBagBag` has a functioning `__bool__`,
        # unlike Python's `Counter`.)
        return fbb.n_elements
    try:
        return cache[(k, fbb)]
    except KeyError:
        pass
    
    levels = []
    current_fbbs = {fbb}
    while len(levels) < k and current_fbbs:
        k_ = k - len(levels)
        levels.append(
            {fbb_: fbb_.get_sub_fbbs_for_one_crate_and_previous_piles_removed()
             for fbb_ in current_fbbs
                                                    if (k_, fbb_) not in cache}
        )
        current_fbbs = set(itertools.chain(*levels[-1].values()))
        
    # The last level is calculated. Time to make our way up.
    for k_, level in enumerate(reversed(levels), (k - len(levels) + 1)):
        if k_ == 1:
            for fbb_, sub_fbbs in level.items():
                cache[(k_, fbb_)] = len(sub_fbbs)
        else:
            for fbb_, sub_fbbs in level.items():
                cache[(k_, fbb_)] = sum(
                    (cache[(k_ - 1, sub_fbb)] for sub_fbb in sub_fbbs)
                )
    
    return cache[(k, fbb)]
        
    
            

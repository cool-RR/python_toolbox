# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

import itertools

from python_toolbox import nifty_collections


_length_of_recurrent_perm_space_cache = {}

def calculate_length_of_recurrent_perm_space(k, fbb):
    '''
    Calculate the length of a recurrent `PermSpace`.
    
    `k` is the `n_elements` of the space, i.e. the length of each perm. `fbb`
    is the space's `FrozenBagBag`, meaning a bag where each key is the number
    of recurrences of an item and each count is the number of different items
    that have this number of recurrences. (See documentation of `FrozenBagBag`
    for more info.)
    
    It's assumed that the space is not a `CombSpace`, it's not fixed, not
    degreed and not sliced.
    '''
    cache = _length_of_recurrent_perm_space_cache
    if not isinstance(fbb, nifty_collections.FrozenBagBag):
        fbb = nifty_collections.FrozenBagBag(fbb)
    ### Checking for edge cases: ##############################################
    #                                                                         #
    if k == 0:
        return 1
    elif k == 1:
        assert fbb
        # (Works because `FrozenBagBag` has a functioning `__bool__`, unlike
        # Python's `Counter`.)
        return fbb.n_elements
    #                                                                         #
    ### Finished checking for edge cases. #####################################
    
    try:
        return cache[(k, fbb)]
    except KeyError:
        pass

    # This is a 2-phase algorithm, similar to recursion but not really
    # recursion since we don't want to abuse the stack.
    #
    # In the first phase, we get all the sub-FBBs that we need to solve for to
    # get a solution for this FBB, and then for these sub-FBBs we get the
    # sub-sub-FBBs we need to solve in order to solve them, and we continue
    # until we reach trivial FBBs.
    #
    # In the second phase, we'll go over the levels of FBBs, starting with the
    # simplest ones and making our way up to the original FBB. The simplest
    # FBBs will be solved trivially, and then as they get progressively more
    # complex, each FBB will be solved using the solutions of its sub-FBB.
    # Every solution will be stored in the global cache.

    
    ### Doing phase one, getting all sub-FBBs: ################################
    #                                                                         #
    levels = []
    current_fbbs = {fbb}
    while len(levels) < k and current_fbbs:
        k_ = k - len(levels)
        levels.append(
            {fbb_: fbb_.get_sub_fbbs_for_one_key_removed()
             for fbb_ in current_fbbs if (k_, fbb_) not in cache}
        )
        current_fbbs = set(itertools.chain(*levels[-1].values()))
    #                                                                         #
    ### Finished doing phase one, getting all sub-FBBs. #######################
    
    ### Doing phase two, solving FBBs from trivial to complex: ################
    #                                                                         #
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
    #                                                                         #
    ### Finished doing phase two, solving FBBs from trivial to complex. #######
    
    return cache[(k, fbb)]
        
    


###############################################################################

_length_of_recurrent_comb_space_cache = {}

def calculate_length_of_recurrent_comb_space(k, fbb):
    '''
    Calculate the length of a recurrent `CombSpace`.
    
    `k` is the `n_elements` of the space, i.e. the length of each perm. `fbb`
    is the space's `FrozenBagBag`, meaning a bag where each key is the number
    of recurrences of an item and each count is the number of different items
    that have this number of recurrences. (See documentation of `FrozenBagBag`
    for more info.)
    
    It's assumed that the space is not fixed, not degreed and not sliced.
    '''
    cache = _length_of_recurrent_comb_space_cache
    if not isinstance(fbb, nifty_collections.FrozenBagBag):
        fbb = nifty_collections.FrozenBagBag(fbb)
    ### Checking for edge cases: ##############################################
    #                                                                         #
    if k == 0:
        return 1
    elif k == 1:
        assert fbb
        # (Works because `FrozenBagBag` has a functioning `__bool__`,
        # unlike Python's `Counter`.)
        return fbb.n_elements
    #                                                                         #
    ### Finished checking for edge cases. #####################################

    try:
        return cache[(k, fbb)]
    except KeyError:
        pass
    
    # This is a 2-phase algorithm, similar to recursion but not really
    # recursion since we don't want to abuse the stack.
    #
    # In the first phase, we get all the sub-FBBs that we need to solve for to
    # get a solution for this FBB, and then for these sub-FBBs we get the
    # sub-sub-FBBs we need to solve in order to solve them, and we continue
    # until we reach trivial FBBs.
    #
    # In the second phase, we'll go over the levels of FBBs, starting with the
    # simplest ones and making our way up to the original FBB. The simplest
    # FBBs will be solved trivially, and then as they get progressively more
    # complex, each FBB will be solved using the solutions of its sub-FBB.
    # Every solution will be stored in the global cache.

    
    ### Doing phase one, getting all sub-FBBs: ################################
    #                                                                         #
    levels = []
    current_fbbs = {fbb}
    while len(levels) < k and current_fbbs:
        k_ = k - len(levels)
        levels.append(
            {fbb_: fbb_.get_sub_fbbs_for_one_key_and_previous_piles_removed()
             for fbb_ in current_fbbs if (k_, fbb_) not in cache}
        )
        current_fbbs = set(itertools.chain(*levels[-1].values()))
    #                                                                         #
    ### Finished doing phase one, getting all sub-FBBs. #######################
        
    ### Doing phase two, solving FBBs from trivial to complex: ################
    #                                                                         #
    for k_, level in enumerate(reversed(levels), (k - len(levels) + 1)):
        if k_ == 1:
            for fbb_, sub_fbbs in level.items():
                cache[(k_, fbb_)] = len(sub_fbbs)
        else:
            for fbb_, sub_fbbs in level.items():
                cache[(k_, fbb_)] = sum(
                    (cache[(k_ - 1, sub_fbb)] for sub_fbb in sub_fbbs)
                )
    #                                                                         #
    ### Finished doing phase two, solving FBBs from trivial to complex. #######
    
    return cache[(k, fbb)]
        
    
            

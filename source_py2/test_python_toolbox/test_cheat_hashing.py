# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `python_toolbox.abc_tools.AbstractStaticMethod`.'''

import copy

from python_toolbox.cheat_hashing import cheat_hash


def test_cheat_hash():
    '''Test `cheat_hash` on various objects.'''
    
    things = [
        1,
        7,
        4.5,
        [1, 2, 3.4],
        (1, 2, 3.4),
        {1: 2, 3: 4.5},
        set((1, 2, 3.4)),
        [1, [1, 2], 3],
        [1, {frozenset((1, 2)): 'meow'}, 3],
        sum,
        None,
        (None, {None: None})
    ]
    
    things_copy = copy.deepcopy(things)
        
    for thing, thing_copy in zip(things, things_copy):
        assert cheat_hash(thing) == cheat_hash(thing) == \
               cheat_hash(thing_copy) == cheat_hash(thing_copy)
        
import copy

from garlicsim.general_misc import cheat_hashing
from garlicsim.general_misc.cheat_hashing import cheat_hash


def test_cheat_hash():
    
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
        sum
    ]
    
    things_copy = copy.deepcopy(things)
        
    for thing, thing_copy in zip(things, things_copy):
        assert cheat_hash(thing) == cheat_hash(thing) == \
               cheat_hash(thing_copy) == cheat_hash(thing_copy)
        

def cheat_hash_object(thing):
    try:
        return hash(thing)
    except Exception:
        return id(thing)

    
def cheat_hash_set(my_set):
    hashables = set()
    unhashables = set()
    for thing in my_set:
        try:
            hash(thing)
        except Exception:
            unhashables.add(thing)
        else:
            hashables.add(thing)
            
    return hash(
        (
            frozenset(hashables),
            tuple(sorted(cheat_hash(thing) for thing in unhashables))
        )
    )    


def cheat_hash_sequence(my_sequence):
    hashables = []
    unhashables = []
    for thing in my_sequence:
        try:
            hash(thing)
        except Exception:
            unhashables.append(thing)
        else:
            hashables.append(thing)
            
    return hash(
        (
            tuple(hashables),
            tuple(cheat_hash(thing) for thing in unhashables)
        )
    )    


def cheat_hash_dict(my_dict):
    hashable_items = []
    unhashable_items = []
    for key, value in my_dict.iteritems():
        try:
            hash((key, value))
        except Exception:
            unhashable_items.append((key, value))
        else:
            hashable_items.append((key, value))
            
    return hash(
        (
            tuple(sorted(hashable_items)),
            tuple(cheat_hash(thing) for thing in sorted(unhashable_items))
        )
    )

from .cheat_hash import cheat_hash
from garlicsim.general_misc.infinity import Infinity

from .cheat_hash_functions import (cheat_hash_dict, cheat_hash_object, 
                                   cheat_hash_sequence, cheat_hash_set)


dispatch_map = {
    object: cheat_hash_object,
    tuple: cheat_hash_sequence,
    list: cheat_hash_sequence,
    dict: cheat_hash_dict,
    set: cheat_hash_set
}


def cheat_hash(thing):
    thing_type = type(thing)
    matching_types = \
        [type_ for type_ in dispatch_map if issubclass(thing_type, type_)]
    
    mro = thing_type.mro()
    
    matching_type = min(
        matching_types,
        key=lambda type_: (mro.index(type_) if type_ in mro else Infinity)
    )
    
    return dispatch_map[matching_type](thing)
    
        
        
            
# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''
Defines the `cheat_hash` function for cheat-hashing mutable objects.

See its documentation for more details.
'''

from .cheat_hash_functions import (cheat_hash_dict, cheat_hash_object, 
                                   cheat_hash_sequence, cheat_hash_set)

infinity = float('inf')

dispatch_map = {
    object: cheat_hash_object,
    tuple: cheat_hash_sequence,
    list: cheat_hash_sequence,
    dict: cheat_hash_dict,
    set: cheat_hash_set
}
'''`dict` mapping from a type to a function that cheat-hashes it.'''


def cheat_hash(thing):
    '''
    Cheat-hash an object. Works on mutable objects.
    
    This is a replacement for `hash` which generates something like an hash for
    an object, even if it is mutable, unhashable and/or refers to
    mutable/unhashable objects.
    
    This is intended for situtations where you have mutable objects that you
    never modify, and you want to be able to hash them despite Python not
    letting you.
    '''
    thing_type = type(thing)
    matching_types = \
        [type_ for type_ in dispatch_map if issubclass(thing_type, type_)]
    
    mro = thing_type.mro()
    
    matching_type = min(
        matching_types,
        key=lambda type_: (mro.index(type_) if type_ in mro else infinity)
    )
    
    return dispatch_map[matching_type](thing)
    
        
        
            
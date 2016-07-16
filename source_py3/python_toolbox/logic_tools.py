# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''This module defines logic-related tools.'''

import collections
import itertools
import operator

from python_toolbox import cute_iter_tools


def all_equivalent(iterable, relation=operator.eq, *, assume_reflexive=True,
                   assume_symmetric=True, assume_transitive=True):
    '''
    Return whether all elements in the iterable are equivalent to each other.
    
    By default "equivalent" means they're all equal to each other in Python.
    You can set a different relation to the `relation` argument, as a function
    that accepts two arguments and returns whether they're equivalent or not.
    You can use this, for example, to test if all items are NOT equal by
    passing in `relation=operator.ne`. You can also define any custom relation
    you want: `relation=(lambda x, y: x % 7 == y % 7)`.
    
    By default, we assume that the relation we're using is an equivalence
    relation (see http://en.wikipedia.org/wiki/Equivalence_relation for
    definition.) This means that we assume the relation is reflexive, symmetric
    and transitive, so we can do less checks on the elements to save time. You
    can use `assume_reflexive=False`, `assume_symmetric=False` and
    `assume_transitive=False` to break any of these assumptions and make this
    function do more checks that the equivalence holds between any pair of
    items from the iterable. (The more assumptions you ask to break, the more
    checks this function does before it concludes that the relation holds
    between all items.)
    '''
    from python_toolbox import sequence_tools
    
    if not assume_transitive or not assume_reflexive:
        iterable = sequence_tools.ensure_iterable_is_sequence(iterable)
        
    if assume_transitive:
        pairs = cute_iter_tools.iterate_overlapping_subsequences(iterable)
    else:
        from python_toolbox import combi
        pairs = tuple(
            iterable * comb for comb in combi.CombSpace(len(iterable), 2)
        )
        # Can't feed the items directly to `CombSpace` because they might not
        # be hashable.
        
    if not assume_symmetric:
        pairs = itertools.chain(
            *itertools.starmap(lambda x, y: ((x, y), (y, x)), pairs)
        )
    
    if not assume_reflexive:
        pairs = itertools.chain(pairs,
                                zip(iterable, iterable))
        
    return all(itertools.starmap(relation, pairs))


def get_equivalence_classes(iterable, key=None, *,
                            big_container=dict, small_container=set):
    '''
    Divide items in `iterable` to equivalence classes, using the key function.
    
    Each item will be put in a set with all other items that had the same
    result when put through the `key` function.
    
    Example:
    
        >>> get_equivalence_classes(range(10), lambda x: x % 3)
        {0: {0, 9, 3, 6}, 1: {1, 4, 7}, 2: {8, 2, 5}}
        
    
    Returns a `dict` with keys being the results of the function, and the
    values being the sets of items with those values.
    
    Alternate usages:
    
        Instead of a key function you may pass in an attribute name as a
        string, and that attribute will be taken from each item as the key.
        
        Instead of an iterable and a key function you may pass in a `dict` (or
        similar mapping) into `iterable`, without specifying a `key`, and the
        value of each item in the `dict` will be used as the key.
        
        Example:
        
            >>> get_equivalence_classes({1: 2, 3: 4, 'meow': 2})
            {2: {1, 'meow'}, 4: {3}}
            
    You can use optional arguments `small_container` and `big_container` to
    customize the containers used in the result. `big_container` is `dict` by
    default, but you can use alternative dict types like `OrderedDict`,
    `defaultdict`, `SortedDict` or any other kind of mapping. Example:
    
        >>> from python_toolbox.nifty_collections import OrderedDict
        >>> get_equivalence_classes(range(10), lambda x: x % 3,
                                    big_container=OrderedDict)
        OrderedDict([(0, {0, 9, 3, 6}), (1, {1, 4, 7}), (2, {8, 2, 5})])
    
    You can pass in either the type of mapping, or an existing instance, and
    then the existing items will still be there and have the equivalence
    classes added to them.
    
    `small_container` is the container in which the items are put inside the
    mapping. By default it's `set` but you can specify any other kind of
    container. If you something like `OrderedSet`, the items will be inserted
    in the same order that they were in the original `iterable`. Example:
    
        >>> get_equivalence_classes(range(10), lambda x: x % 3,
                                    small_container=tuple)
        {0: (0, 3, 6, 9), 1: (1, 4, 7), 2: (2, 5, 8)}

    '''
    from python_toolbox import comparison_tools
    from python_toolbox import nifty_collections
    
    if isinstance(big_container, collections.abc.Mapping):
        big_container_type = type(big_container)
        big_container_instance = big_container
    else:
        big_container_type = big_container
        big_container_instance = None
        assert issubclass(big_container_type, collections.abc.Mapping)
        
    assert issubclass(small_container, collections.abc.Iterable)
    if key is None:
        if isinstance(iterable, collections.abc.Mapping):
            items = iterable.items()
        else:
            raise Exception(
                "You can't put in a non-dict without also supplying a "
                "`key` function. We need to know which key to use."
            )
    else: # key is not None
        assert cute_iter_tools.is_iterable(iterable)
        key_function = comparison_tools.process_key_function_or_attribute_name(
            key
        )
        items = ((key, key_function(key)) for key in iterable)
    
    # If we know our big container isn't ordered, we can save some performance
    # and use a dict as our pre-dict, otherwise play it safe and use an ordered
    # dict.
    pre_dict = ({} if big_container_type in {dict, collections.defaultdict}
                else nifty_collections.OrderedDict())
    for key, value in items:
        pre_dict.setdefault(value, []).append(key)

    if big_container_instance is None:
        big_container_instance = big_container_type(
            ((key, small_container(value)) for key, value in pre_dict.items())
        )
    else:
        for key, value in pre_dict.items():
            big_container_instance[key] = small_container(value)
        
    return big_container_instance
        
      
def logic_max(iterable, relation=lambda a, b: (a >= b)):
    '''
    Get a list of maximums from the iterable.
    
    That is, get all items that are bigger-or-equal to all the items in the
    iterable.
    
    `relation` is allowed to be a partial order.
    '''
    sequence = list(iterable)
    
    maximal_elements = []
    
    for candidate in sequence:
        if all(relation(candidate, thing) for thing in sequence):
            maximal_elements.append(candidate)
    
    return maximal_elements
        
        
        
    
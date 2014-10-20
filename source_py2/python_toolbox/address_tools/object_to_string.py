# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Module for describing Python objects as strings.'''

import types
import re

from python_toolbox import dict_tools
from python_toolbox import caching

# Doing at bottom:
# from .string_to_object import _get_object_by_address, resolve
from .shared import (_address_pattern, _contained_address_pattern,
                     _get_parent_and_dict_from_namespace)

# maybe todo: when shortening, check that we're not using stuff that was
# excluded from `__all__`(if one exists.)


_unresolvable_string_pattern = re.compile("<[^<>]*?'[^<>]*?'[^<>]*?>")
'''Pattern for unresorvable strings, like "<type 'list'>".'''


_address_in_unresolvable_string_pattern = re.compile("[^']*?'([^']*?)'[^']*?")
'''
Pattern for extracting address from unresorvable strings.

For example, matching "type 'list'" would result in `match.groups() ==
('list',)`.
'''


def describe(obj, shorten=False, root=None, namespace={}):
    '''
    Describe a Python object has a string.
    
    For example:

        >>> describe([1, 2, {3: email.encoders}])
        '[1, 2, {3: 4}]'
    
    
    All the parameters are used for trying to give as short of a description as
    possible. The shortening is done only for addresses within the string.
    (Like 'email.encoders'.)
    
    `shorten=True` would try to skip redundant intermediate nodes. For example,
    if asked to describe `django.db.utils.ConnectionRouter` with `shorten` on,
    it will return 'django.db.ConnectionRouter', because the `ConnectionRouter`
    class is available at this shorter address as well.
    
    The parameters `root` and `namespace` help shorten addresses some more.
    It's assumed we can express any address in relation to `root`, or in
    relation to an item in `namespace`. For example, if `root=python_toolbox`
    or `namespace=python_toolbox.__dict__`, we could describe
    `python_toolbox.caching` as simply 'caching'.)
    '''
    
    # If it's the easy case of a module/function/class or something like that,
    # we solve it by simply using `get_address`:
    if isinstance(obj, types.ModuleType) or \
       (hasattr(obj, '__module__') and hasattr(obj, '__name__')):
        
        return get_address(obj, shorten=shorten, root=root,
                            namespace=namespace)
    
    
    # What we do is take a `repr` of the object, and try to make it less ugly.
    # For example, given the object `{3: email.encoders}`:
    raw_result = repr(obj)
    # Our `raw_result` would be "{3: <module 'email.encoders' from
    # 'c:\Python25\lib\email\encoders.pyc'>}", which is not pretty at all. Our
    # goal is to take all these <nasty parts> from that string and replacing
    # them with the actual addresses of the objects, if possible.
    
    current_result = raw_result
        
    while True:

        current_result_changed = False
        
        ugly_reprs = _unresolvable_string_pattern.findall(current_result)
        
        for ugly_repr in ugly_reprs:
            # An `ugly_repr` is something like "<type 'list'>"
            
            # We try to extract an address from it:...
            re_match = _address_in_unresolvable_string_pattern.match(ugly_repr)
        
            # ...But if we can't, we just let it go ugly:
            if not re_match:
                continue
            
            address_of_ugly_repr = re_match.groups()[0]
            
            try:
                object_candidate = get_object_by_address(address_of_ugly_repr)
                # (Not using `root` and `namespace` cause it's an address
                # manufactured by `repr`.)
            except Exception:
                continue
            

            if repr(object_candidate) == ugly_repr:

                # We have a winner! We found the actual object that this
                # `ugly_repr` was trying to refer to:
                object_winner = object_candidate
                
                # Let's replace `ugly_repr` with the actual address of the
                # object:
                pretty_address = get_address(object_winner, root=root,
                                              namespace=namespace)
                current_result = current_result.replace(ugly_repr,
                                                        pretty_address)
                current_result_changed = True
          
        if current_result_changed:
            # We `continue` on the while loop, just in case some `ugly_repr` we
            # might be able to fix is still there:
            continue
        
        break
    
    return current_result


@caching.cache()
def get_address(obj, shorten=False, root=None, namespace={}):
    '''
    Get the address of a Python object.
    
    This only works for objects that have addresses, like modules, classes,
    functions, methods, etc. It usually doesn't work on instances created
    during the program. (e.g. `[1, 2]` doesn't have an address.)
    '''
    # todo: Support classes inside classes. Currently doesn't work because
    # Python doesn't tell us inside in which class an inner class was defined.
    # We'll probably have to do some kind of search.
    
    if not (isinstance(obj, types.ModuleType) or hasattr(obj, '__module__')):
        raise TypeError("`%s` is not a module, nor does it have a "
                        "`.__module__` attribute, therefore we can't get its "
                        "address." % (obj,))
    
    if isinstance(obj, types.ModuleType):
        address = obj.__name__
    elif isinstance(obj, types.MethodType):
        address = '.'.join((obj.__module__, obj.im_class.__name__,
                            obj.__name__))
    else:
        address= '.'.join((obj.__module__, obj.__name__))

    # Now our attempt at an address is in `address`. Let's `try` to resolve
    # that address to see if it's right and we get the same object:        
    try:
        object_candidate = get_object_by_address(address)
    except Exception:
        confirmed_object_address = False 
    else:
        is_same_object = \
            (obj == object_candidate) if isinstance(obj, types.MethodType) \
            else (obj is object_candidate)
        confirmed_object_address = is_same_object
        
    if not confirmed_object_address:
        # We weren't able to confirm that the `address` we got is the correct
        # one for this object, so we won't even try to shorten it in any way,
        # just return what we got and hoped we didn't disappoint the user too
        # badly:
        return address

    assert confirmed_object_address is True
    # We confirmed we got the right `address`! Now we can try to shorten it
    # some, if the user specified so in the arguments:

    ### Shortening the address using `root` and/or `namespace`: ###############
    #                                                                         #
    
    if root or namespace:
        
        # Ensuring `root` and `namespace` are actual objects:
        if isinstance(root, basestring):
            root = get_object_by_address(root)            
        if isinstance(namespace, basestring):
            namespace = get_object_by_address(namespace)


        if namespace:
            
            (_useless, original_namespace_dict) = \
                _get_parent_and_dict_from_namespace(namespace)
            
            def my_filter(key, value):
                name = getattr(value, '__name__', '')
                return isinstance(name, basestring) and name.endswith(key)

            namespace_dict = dict_tools.filter_items(
                original_namespace_dict,
                my_filter
            )
                
            namespace_dict_keys = namespace_dict.keys()
            namespace_dict_values = namespace_dict.values()
            
            
        # Split to address parts:
        address_parts = address.split('.')
        # e.g., `['python_toolbox', 'misc', 'step_copy', 'StepCopy']`.
        
        heads = ['.'.join(address_parts[:i]) for i in
                 xrange(1, len(address_parts) + 1)]
        # `heads` is something like: `['python_toolbox',
        # 'python_toolbox.caching', 'python_toolbox.caching.cached_type',
        # 'python_toolbox.cached_type.CachedType']`

        
        for head in reversed(heads):
            object_ = get_object_by_address(head)
            if root:
                if object_ is root:
                    root_short_name = root.__name__.rsplit('.', 1)[-1]
                    address = address.replace(head, root_short_name, 1)
                    break
            if namespace:
                if object_ in namespace_dict_values:
                    fitting_keys = [key for key in namespace_dict_keys if
                                    namespace_dict[key] is object_]
                    key = min(fitting_keys, key=len)
                    address = address.replace(head, key, 1)

    #                                                                         #
    ### Finshed shortening address using `root` and/or `namespace`. ###########
                    

    # If user specified `shorten=True`, let the dedicated `shorten_address`
    # function drop redundant intermediate nodes:
    if shorten:
        address = shorten_address(address, root=root, namespace=namespace)
        
    
    # A little fix to avoid describing something like `list` as
    # `__builtin__.list`:
    if address.startswith('__builtin__.'):
        shorter_address = address.replace('__builtin__.', '', 1)
        if get_object_by_address(shorter_address) == obj:
            address = shorter_address

            
    return address


def shorten_address(address, root=None, namespace={}):
    '''
    Shorten an address by dropping redundant intermediate nodes.
    
    For example, 'python_toolbox.caching.cached_property.CachedProperty' could
    be shortened to 'python_toolbox.caching.CachedProperty', because the
    `CachedProperty` class is available at this shorter address as well.
    
    Note: `root` and `namespace` are only provided in order to access the
    object. This function doesn't do root- or namespace-shortening.
    '''

    assert _address_pattern.match(address)
    
    if '.' not in address:
        # It's a single-level address; nothing to shorten.
        return address
    
    original_address_parts = address.split('.')
    address_parts = original_address_parts[:]
    
    new_address = address
    
    for i in range(2 - len(original_address_parts), 1):
        
        if i == 0:
            i = None
            # Yeah, this is weird. When `i == 0`, I want to slice `[:i]` and
            # get everything. So I change `i` to `None`.
            
        head = '.'.join(address_parts[:i])

        # Let me explain what `head` is. Assume we got an address of
        # `a.b.c.d.e`, which is shortable to `a.b.d.e`. (Dropping the `c`
        # node.) So in this for loop we're iterating over the differnt "heads"
        # of the address. So `head` will first be `a.b`, then on the next
        # iteration `a.b.c`, then `a.b.c.d`, then finally `a.b.c.d.e`. (We're
        # skipping the first head `a` because a single-level address can't be
        # shortened.)
        
        # For every `head`, we try to `_tail_shorten` it:
        new_head = _tail_shorten(head, root=root, namespace=namespace)
        
        if new_head != head:
            # Tail-shortening was successful! So something like `a.b.c.d` was
            # shortened to `a.b.d`. We replace the old address with the new
            # short one:
            new_address = new_address.replace(head, new_head, 1)
            address_parts = address.split('.')
            
    # After we looped on all the different possible heads of the address and
    # tail-shortened each of them that we can, `new_address` has the
    # maximally-shortened address:
    return new_address


def _tail_shorten(address, root=None, namespace={}):
    '''
    Shorten an address by eliminating tails. Internal function.
    
    When we say tail here, we mean a tail ending just before the final node of
    the address, not including the final one. For example, the tails of
    'a.b.c.d.e' would be 'd', 'c.d', 'b.c.d' and 'a.b.c.d'.
    
    For example, if given an address 'a.b.c.d.e', we'll check if we can access
    the same object with 'a.b.c.e'. If so we try 'a.b.e'. If so we try 'a.e'.
    When it stops working, we take the last address that worked and return it.
    
    Note: `root` and `namespace` are only provided in order to access the
    object. This function doesn't do root- or namespace-shortening.
    '''
    if '.' not in address:
        # Nothing to shorten
        return address
    
    parent_address, child_name = address.rsplit('.', 1)
    child = get_object_by_address(address, root=root, namespace=namespace)
    
    current_parent_address = parent_address
    
    last_successful_parent_address = current_parent_address
    
    while True:
        # Removing the last component from the parent address:
        current_parent_address = '.'.join(
            current_parent_address.split('.')[:-1]
        )
        
        if not current_parent_address:
            # We've reached the top module and it's successful, can break now.
            break
        
        current_parent = get_object_by_address(current_parent_address,
                                               root=root,
                                               namespace=namespace)
        
        candidate_child = getattr(current_parent, child_name, None)
        
        if candidate_child is child:
            last_successful_parent_address = current_parent_address
        else:
            break
        
    return '.'.join((last_successful_parent_address, child_name))

    
from .string_to_object import get_object_by_address, resolve
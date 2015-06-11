# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Module for resolving strings into Python objects.'''

import types

from python_toolbox import dict_tools
from python_toolbox import re_tools

from .shared import (_contained_address_pattern, _address_pattern,
                     _get_parent_and_dict_from_namespace)


def resolve(string, root=None, namespace={}):
    r'''
    Resolve an address into a Python object. A more powerful version of `eval`.
    
    The main advantage it has over `eval` is that it automatically imports
    whichever modules are needed to resolve the string.
    
    For example:
    
        >>> address_tools.resolve('[list, [1, 2], email]')
        [<type 'list'>, [1, 2], <module 'email' from
        'c:\Python27\lib\email\__init__.pyc'>]
        
    `root` is an object (usually a module) whose attributes will be looked at
    when searching for the object. `namespace` is a `dict` whose keys will be
    searched as well.
    '''
    
    # Resolving '' to `None`:
    if string == '':
        return None
    
    # If the string is a simple address, like 'email.encoders', our job is
    # easy:
    if _address_pattern.match(string):        
        return get_object_by_address(string, root=root, namespace=namespace)

    # Getting the true namespace `dict`:
    (_useless, namespace_dict) = _get_parent_and_dict_from_namespace(namespace)
    
    # We're putting items into `our_namespace` instead of using the given
    # namespace `dict`:...
    our_namespace = {}
    our_namespace.update(namespace_dict)
    # ...because we intend to modify it, and we don't want to be modifying the
    # user's arguments.
    
    # The string that we have is not a plain address, but it may contain plain
    # addresses. For example, '{email.encoders: 1}' contains an address. We
    # find all these contained addresses:
    re_matches = re_tools.searchall(_contained_address_pattern, string)
    addresses = [re_match.group('address') for re_match in re_matches]
    
    # We make sure all the addresses are (1) imported and (2) in
    # `our_namespace` dict, so we could access them when we `eval` the string:
    for address in addresses:
        try:
            get_object_by_address(address, root=root, namespace=namespace)
        except Exception:
            pass
        else:
            big_parent_name = address.split('.', 1)[0] 
            big_parent = get_object_by_address(big_parent_name, root=root,
                                                namespace=namespace)
            our_namespace[big_parent_name] = big_parent
            
    
    return eval(string, our_namespace)
    

def get_object_by_address(address, root=None, namespace={}):
    '''
    Get an object by its address.
    
    For example:
    
        >>> get_object_by_address('email.encoders')
        <module 'email.encoders' from 'c:\Python27\lib\email\encoders.pyc'>
    
    `root` is an object (usually a module) whose attributes will be looked at
    when searching for the object. `namespace` is a `dict` whose keys will be
    searched as well.    
    '''
    # todo: should know what exception this will raise if the address is bad /
    # object doesn't exist.
    
    from python_toolbox import import_tools # Avoiding circular import.
    
    if not _address_pattern.match(address):
        raise ValueError("'%s' is not a legal address." % address)
    
    ###########################################################################
    # Before we start, we do some pre-processing of `root` and `namespace`:   #
    
    # We are letting the user input (base)strings for `root` and `namespace`,
    # so if he did that, we'll get the actual objects.
    
    if root:
        # First for `root`:
        if isinstance(root, str):
            root = get_object_by_address(root)
        root_short_name = root.__name__.rsplit('.', 1)[-1]
        
    if namespace not in (None, {}):
        # And then for `namespace`:
        if isinstance(namespace, str):
            namespace = get_object_by_address(namespace)
            
        parent_object, namespace_dict = _get_parent_and_dict_from_namespace(
            namespace
        )
    else:
        parent_object, namespace_dict = None, None
            
        
    # Finished pre-processing `root` and `namespace`.                         #
    ###########################################################################
    
    
    ###########################################################################
    # The implementation is recursive: We handle the case of a single-level
    # address, like 'email'. If we get a multi-level address (i.e. contains a
    # dot,) like 'email.encoders', we use this function twice, first to get
    # `email`, and then from it to get `email.encoders`.
    
    if '.' not in address:
        
        ### Here we solve the basic case of a single-level address: ###########
        #                                                                     #
        
        # Let's rule out the easy option that the requested object is the root:
        if root and (address == root_short_name):
            return root
    
        if parent_object is not None:
    
            if isinstance(parent_object, types.ModuleType) and \
               hasattr(parent_object, '__path__'):
                                
                # `parent_object` is a package. The wanted object may be a
                # module. Let's try importing it:
                
                import_tools.import_if_exists(
                    '.'.join((parent_object.__name__, address)),
                    silent_fail=True
                )
                # Not keeping reference, just importing so we could get later.
        
        # We know we have a `namespace_dict` to take the object from, and we
        # might have a `parent_object` we can take the object from by using
        # `getattr`. We always have a `namespace_dict`, but not always a
        # `parent_object`.
        #
        
        
        # We are going to prefer to do `getattr` from `parent_object`, if one
        # exists, rather than using `namespace_dict`. This is because some
        # attributes may not be present on an object's `__dict__`, and we want
        # to be able to catch them:
        
        # The first place we'll try to take the object from is the
        # `parent_object`. We try this before `namespace_dict` because
        # `parent_object` may have `__getattr__` or similar magic and our
        # object might be found through that:
        if (parent_object is not None) and hasattr(parent_object, address):
            return getattr(parent_object, address)
        
        # Next is the `namespace_dict`:
        elif namespace_dict and (address in namespace_dict):
            return namespace_dict[address]
        
        # Last two options:
        else:
            try:
                # It may be a built-in:
                return eval(address) 
            except Exception:
                # Or a module:
                return import_tools.normal_import(address)
        
        #                                                                     #
        ### Finished solving the basic case of a single-level address. ########
            
        
    else: # '.' in address
        
        ### If we get a composite address, we solve recursively: ##############
        #                                                                     #
        
        first_object_address, second_object_address = address.rsplit('.', 1)
        
        first_object = get_object_by_address(first_object_address, root=root,
                                             namespace=namespace)

        second_object = get_object_by_address(second_object_address,
                                              namespace=first_object)
        
        return second_object
    
        #                                                                     #
        ### Finished solving recursively for a composite address. #############
        
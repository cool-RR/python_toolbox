import types
import re

from garlicsim.general_misc import import_tools
from garlicsim.general_misc import dict_tools
from garlicsim.general_misc import re_tools
from garlicsim.general_misc import caching

# Doing at bottom:
# from . import object_to_string
from .shared import (_contained_address_pattern, _address_pattern,
                     _get_parent_and_dict_from_namespace)


# blocktododoc: add caching to some functions


def _get_object_by_address(address, root=None, namespace={}):
    
    # blocktododoc: unprivatize since is useful for user

    # todo: should know what exception this will raise if the address is bad /
    # object doesn't exist.
    
    if not _address_pattern.match(address):
        raise ValueError("'%s' is not a legal address." % address)
        # blocktododoc change to assert
    
    ###########################################################################
    # Before we start, we do some analysis of `root` and `namespace`:
    
    # We are letting the user inputs (base)strings for `root` and `namespace`,
    # so if he did that, we'll get the actual objects.
    
    if root:
        # First for `root`:
        if isinstance(root, basestring):
            root = _get_object_by_address(root)
        root_short_name = root.__name__.rsplit('.', 1)[-1]
        
    if namespace:
        # And then for `namespace`:
        if isinstance(namespace, basestring):
            namespace = _get_object_by_address(namespace)
            
        parent_object, namespace_dict = _get_parent_and_dict_from_namespace(
            namespace
        )
    else:
        parent_object, namespace_dict = None, None
            
        
    # Finished analyzing `root` and `namespace`.
    ###########################################################################
    
    # Let's rule out the easy option that the requested object is the root:
    
    
    if '.' not in address:
    
        if root and (address == root_short_name):
            return root
    
        if parent_object:
                
            if isinstance(parent_object, types.ModuleType) and \
               hasattr(parent_object, '__path__'):
                                
                # `parent_object` is a package. The wanted object may be a
                # module. Let's try importing it:
                
                import_tools.import_if_exists(
                    '.'.join((parent_object.__name__, address)),
                    silent_fail=True
                )
                # Not keeping reference, just importing so we could get later
        
        # We know we have a `namespace_dict` to take the object from, and we
        # might have a `parent_object` we can take the object from by using
        # `getattr`. We always have a `namespace_dict`, but not always a
        # `parent_object`.
        #
        # We are going to prefer to do `getattr` from `parent_object`, if one
        # exists, rather than using `namespace_dict`. This is because some
        # attributes may not be present on an object's `__dict__`, and we want
        # to be able to catch them:
        if parent_object and hasattr(parent_object, address):
            return getattr(parent_object, address)
        elif namespace_dict and (address in namespace_dict):
            return namespace_dict[address]
        else:
            try:
                return eval(address) # In case it's a builtin.
            except:
                return __import__(address) # Last option: A module
    
            
    else: # '.' in address
        
        first_object_address, second_object_address = address.rsplit('.', 1)
        
        first_object = _get_object_by_address(first_object_address, root=root,
                                              namespace=namespace)

        second_object = _get_object_by_address(second_object_address,
                                                   namespace=first_object)

        return second_object
    

def resolve(string, root=None, namespace={}):
    # sktechy for now
    # blocktododoc: make sure namespace works here
    # blocktododoc: write tests for this
    
    # Resolving '' to None:
    if string == '':
        return None
    
    if _address_pattern.match(string):
        return _get_object_by_address(string, root=root, namespace=namespace)

    (_useless, namespace_dict) = _get_parent_and_dict_from_namespace(namespace)
    
    our_namespace = {}
    our_namespace.update(namespace_dict)
    
    re_matches = re_tools.searchall(_contained_address_pattern, string)
    addresses = [re_match.group('address') for re_match in re_matches]
    
    for address in addresses:
        try:
            thing = _get_object_by_address(address, root=root,
                                           namespace=namespace)
        except Exception:
            pass
        else:
            big_parent_name = address.split('.', 1)[0]
            big_parent = _get_object_by_address(big_parent_name, root=root,
                                                namespace=namespace)
            our_namespace[big_parent_name] = big_parent
            
    return eval(string, our_namespace)
    

from . import object_to_string
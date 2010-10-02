import types
import re

from garlicsim.general_misc import import_tools
from garlicsim.general_misc import dict_tools
from garlicsim.general_misc import re_tools
from garlicsim.general_misc import caching

# Doing at bottom:
# from .object_to_string import describe, _get_address
from .shared import _address_pattern, _get_parent_and_dict_from_namespace


# tododoc: add caching to all functions, after fixing caching with
# ArgumentsProfile to accept kwargs.


def _get_object_by_address(address, root=None, namespace={}):

    # todo: should know what exception this will raise if the address is bad /
    # object doesn't exist.
    
    if not _address_pattern.match(address):
        raise ValueError("'%s' is not a legal address." % address)
    
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
            
        
    # Finished analyzing `root` and `namespace`.
    ###########################################################################
    
    # Let's rule out the easy option that the requested object is the root:
    if root and (address == root_short_name):
        return root
    
    
    if not namespace:
        
        if '.' not in address:
            # We were called without a namespace with an address with no dots.
            # There are limited options on what it can be: Either the root (we
            # ruled that out above), or a builtin, or a module. We try the last
            # two:
            try:
                return eval(address) # Option 1: A builtin.
            except NameError:
                return __import__(address) # Option 2: A module.
                
        else: # '.' in address
            first_object_address, second_object_address = \
                address.rsplit('.', 1)
            first_object = _get_object_by_address(first_object_address,
                                                  root=root)
            second_object = _get_object_by_address(second_object_address,
                                       namespace=first_object)
            return second_object

        
    else: # We got a namespace
        
        if '.' not in address:
            
            if parent_object:
                
                if isinstance(parent_object, types.ModuleType) and \
                   hasattr(parent_object, '__path__'):
                                    
                    # `parent_object` is a package. The wanted object may be a
                    # module. Let's try importing it:
                    
                    import_tools.import_if_exists(
                        '.'.join((parent_object.__name__, address)),
                        silent_fail=True
                    )
                    # Not keeping reference, just importing so we could get
                    # later
            
            # We know we have a `namespace_dict` to take the object from, and we
            # might have a `parent_object` we can take the object from by using
            # `getattr`. We always have a `namespace_dict`, but not always a
            # `parent_object`.
            #
            # We are going to prefer to do `getattr` from `parent_object`, if
            # one exists, rather than using `namespace_dict`. This is because
            # some attributes may not be present on an object's `__dict__`, and
            # we want to be able to catch them:
            if parent_object:
                return getattr(parent_object, address)
            else:
                return namespace_dict[address]
        
        else: # '.' in address
            first_object_address, second_object_address = \
                address.rsplit('.', 1)
            first_object = _get_object_by_address(
                first_object_address,
                root=root,
                namespace=parent_object or namespace_dict
            )
            second_object = _get_object_by_address(
                second_object_address,
                namespace=first_object
            )
            return second_object
    

def resolve(string, root=None, namespace={}):
    # sktechy for now
    # tododoc: make sure namespace works here
    # tododoc: write tests for this
    
    # Resolving '' to None:
    if string == '':
        return None
    
    if _address_pattern.match(string):
        return _get_object_by_address(string, root=root, namespace=namespace)

    (_useless, namespace_dict) = _get_parent_and_dict_from_namespace(namespace)
    
    our_namespace = {}
    our_namespace.update(namespace_dict)
    
    re_matches = re_tools.searchall(_address_pattern, string)
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
    

from .object_to_string import describe, _get_address
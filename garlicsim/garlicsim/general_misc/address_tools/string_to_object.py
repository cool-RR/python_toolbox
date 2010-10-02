import types
import re

from garlicsim.general_misc import import_tools
from garlicsim.general_misc import dict_tools
from garlicsim.general_misc import caching

# Doing at bottom:
# from .object_to_string import describe, _get_address
from .shared import _address_pattern

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
        
        # For the namespace, the user can give either a parent object
        # (`getattr(namespace, address) is obj`) or a dict-like namespace
        # (`namespace[address] is obj`).
        #
        # Here we extract the actual namespace and call it `namespace_dict`:
            
        if hasattr(namespace, '__getitem__') and hasattr(namespace, 'keys'):
            parent_object = None
            namespace_dict = namespace
            
        else:
            parent_object = namespace
            namespace_dict = vars(parent_object)
            
        
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
    

def resolve(address, root=None, namespace={}):
    # sktechy for now
    # tododoc: make sure namespace works here
    # tododoc: write tests for this
    
    # Resolving '' to None:
    if address == '':
        return None
    
    try:
        return eval(address)
    except (NameError, AttributeError):
        return _get_object_by_address(address, root, namespace)
    

from .object_to_string import describe, _get_address
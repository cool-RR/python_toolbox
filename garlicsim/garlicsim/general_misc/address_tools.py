import types

from garlicsim.general_misc import import_tools
from garlicsim.general_misc import caching

# tododoc: add caching to all functions, after fixing caching with
# ArgumentsProfile to accept kwargs.

# todo: when shortening, check that we're not using stuff that was excluded from
# `__all__` (if one exists)


def _tail_shorten(address, root=None, namespace={}):
    '''
    '''
    if '.' not in address:
        # Nothing to shorten
        return address
    
    parent_address, child_name = address.rsplit('.', 1)
    parent = get_object(parent_address, root=root, namespace=namespace)
    child = get_object(address, root=root, namespace=namespace)
    
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
        
        current_parent = get_object(current_parent_address,
                                    root=root, namespace=namespace)
        
        candidate_child = getattr(current_parent, child_name, None)
        
        if candidate_child is child:
            last_successful_parent_address = current_parent_address
        else:
            break
        
    return '.'.join((last_successful_parent_address, child_name))


def shorten_address(address, root=None, namespace={}):
    '''
    
    Note: does shortening by dropping intermediate nodes, doesn't do
    root-shortening
    '''
    if '.' not in address:
        # Nothing to shorten
        return address
    
    original_address_parts = address.split('.')
    address_parts = original_address_parts[:]
    
    new_address = address
    
    for i in range(2 - len(original_address_parts), 1):
        
        if i == 0:
            i = None
            # Yeah, this is weird. When `i == 0`, I want to slice `[:i]` and get
            # everything. So I change `i` to `None`.
            
        head = '.'.join(address_parts[:i])
        new_head = _tail_shorten(head, root=root, namespace=namespace)
        if new_head != head:
            # Something was shortened!
            new_address = new_address.replace(head, new_head, 1)
            address_parts = address.split('.')
            
    return new_address


def get_object(address, root=None, namespace={}):

    # todo: should know what exception this will raise if the address is bad /
    # object doesn't exist.
    # todo: probably allow `namespace` argument
    
    ###########################################################################
    # Before we start, we do some analysis of `root` and `namespace`:
    
    # We are letting the user inputs (base)strings for `root` and `namespace`,
    # so if he did that, we'll get the actual objects.
    
    if root:
        # First for `root`:
        if isinstance(root, basestring):
            root = get_object(root)
        root_short_name = root.__name__.rsplit('.', 1)[-1]
        
    if namespace:
        # And then for `namespace`:
        if isinstance(namespace, basestring):
            namespace = get_object(namespace)
        
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
    
    if not namespace:
        
        if '.' not in address:
            # We were called directly by the user with an address with no dots.
            # There are limited options on what it can be: Either the root, or a
            # builtin, or a module. We try all three:
            if root and (address == root_short_name):
                return root # Option 1: The root.
            else:
                try:
                    return eval(address) # Option 2: A builtin.
                except NameError:
                    return __import__(address) # Option 3: A module.
                
        else: # '.' in address
            first_object_address, second_object_address = \
                address.rsplit('.', 1)
            first_object = get_object(first_object_address, root=root)
            second_object = get_object(second_object_address,
                                       namespace=first_object)
            return second_object

        
    else: # We got a namespace
        
        if '.' not in address:
            
            if isinstance(_parent_object, types.ModuleType) and \
               hasattr(_parent_object, '__path__'):
                                
                # `_parent_object` is a package. The wanted object may be a
                # module. Let's try importing it:
                
                import_tools.import_if_exists(
                    '.'.join((_parent_object.__name__, address)),
                    silent_fail=True
                )
                # Not keeping reference, just importing so we could get later
                
            return getattr(_parent_object, address)
        
        else: # '.' in address
            first_object_address, second_object_address = \
                address.rsplit('.', 1)
            first_object = get_object(first_object_address, _parent_object)
            second_object = get_object(second_object_address,
                                       _parent_object=first_object)
            return second_object
    

def get_address(obj, shorten=False, root=None, namespace={}):
    
    # todo: Support classes inside classes. Currently doesn't work because
    # Python doesn't tell us inside in which class an inner class was defined.
    # We'll probably have to do some kind of search.
    
    if not (isinstance(obj, types.ModuleType) or hasattr(obj, '__module__')):
        raise Exception("%s is not a module, nor does not have a `__module__` "
                        "attribute, therefore we can't get its address." % \
                        obj)
    
    if isinstance(obj, types.ModuleType):
        address = obj.__name__
        assert get_object(address) is obj
    
    elif isinstance(obj, types.MethodType):
        address = '.'.join((obj.__module__, obj.im_class.__name__,
                            obj.__name__))
        assert get_object(address) == obj
        
    else:
        address= '.'.join((obj.__module__, obj.__name__))
        assert get_object(address) is obj
        
        
    if root or namespace:
        
        if isinstance(root, basestring):
            root = get_object(root)
            
        if isinstance(namespace, basestring):
            namespace = get_object(namespace)

            
        if hasattr(namespace, '__getitem__') and hasattr(namespace, 'keys'):
            namespace_dict = namespace
        else:
            namespace_dict = vars(namespace)
        
        namespace_dict_keys = namespace_dict_values.keys()
        namespace_dict_values = namespace_dict_values.values()

        
        address_parts = address.split('.')
        heads = ['.'.join(address_parts[:i]) for i in
                 range(1, len(address_parts) + 1)]
        # heads is something like: ['garlicsim', 'garlicsim.misc',
        # 'garlicsim.misc.step_copy', 'garlicsim.misc.step_copy.StepCopy']
        
        for head in reversed(heads):
            object_ = get_object(head)
            if object_ is root:
                root_short_name = root.__name__.rsplit('.', 1)[-1]
                address = address.replace(head, root_short_name, 1)
                break
            elif object_ in namespace_dict_values:
                fitting_keys = [key for key in namespace_dict_keys if 
                                namespace_dict[key] is object_]
                key = min(fitting_keys, len)
                address = address.replace(head, key, 1)
                
    if shorten:
        address = shorten_address(address, root=root, namespace=namespace)
    
    return address


def resolve(address, root=None, namespace={}):
    # sktechy for now    
    # tododoc: create reverse. repr won't do because it puts <> around classes
    # and stuff
    # tododoc: make sure namespace works here
    
    # Resolving '' to None:
    if address == '':
        return None
    
    try:
        return eval(address)
    except (NameError, AttributeError):
        return get_object(address, root)
    
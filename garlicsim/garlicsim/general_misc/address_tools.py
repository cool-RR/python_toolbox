import types

from garlicsim.general_misc import import_tools
from garlicsim.general_misc import caching

# tododoc: add caching to all functions, after fixing caching with
# ArgumentsProfile to accept kwargs.


def _tail_shorten(address, root=None):
    '''
    '''
    if '.' not in address:
        # Nothing to shorten
        return address
    
    parent_address, child_name = address.rsplit('.', 1)
    parent = get_object_by_address(parent_address, root=root)
    child = get_object_by_address(address, root=root)
    
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
                                               root=root)
        
        candidate_child = getattr(current_parent, child_name, None)
        
        if candidate_child is child:
            last_successful_parent_address = current_parent_address
        else:
            break
        
    return '.'.join((last_successful_parent_address, child_name))


def shorten_address(address, root=None):
    '''
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
        new_head = _tail_shorten(head, root=root)
        if new_head != head:
            # Something was shortened!
            new_address = new_address.replace(head, new_head, 1)
            address_parts = address.split('.')
            
    return new_address


def get_object_by_address(address, root=None, _parent_object=None):
    
    if root:        
        if isinstance(root, basestring):
            root = get_object_by_address(root)
        root_short_name = root.__name__.rsplit('.', 1)[-1]
    
    if not _parent_object:
        # We were called directly by the user.
        
        if '.' not in address:
            # We were called directly by the user with an address with no dots.
            # There are limited options on what it can be: Either the root, or a
            # builtin, or a module. We try all three:
            if root and (address == root_short_name):
                return root
            else:
                try:
                    return eval(address)
                except NameError:
                    return __import__(address)
                
        else: # '.' in address
            first_object_address, second_object_address = \
                address.rsplit('.', 1)
            first_object = get_object_by_address(first_object_address,
                                                 root=root)
            second_object = get_object_by_address(second_object_address,
                                                  _parent_object=first_object)
            return second_object

        
    else: # _parent_object is not none
        
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
            first_object = get_object_by_address(first_object_address, _parent_object)
            second_object = get_object_by_address(second_object_address,
                                                  _parent_object=first_object)
            return second_object
    

def get_address(obj, root=None, shorten=None):
    
    # todo: Support classes inside classes. Currently doesn't work because
    # Python doesn't tell us inside in which class an inner class was defined.
    # We'll probably have to do some kind of search.
    
    if not (isinstance(obj, types.ModuleType) or hasattr(obj, '__module__')):
        raise Exception("%s is not a module, nor does not have a `__module__` "
                        "attribute, therefore we can't get it's address." % \
                        obj)
    
    if isinstance(obj, types.ModuleType):
        address = obj.__name__
        assert get_object_by_address(address) is obj
    
    elif isinstance(obj, types.MethodType):
        address = '.'.join((obj.__module__, obj.im_class.__name__,
                                      obj.__name__))
        assert get_object_by_address(address) == obj
        
    else:
        address= '.'.join((obj.__module__, obj.__name__))
        assert get_object_by_address(address) is obj
        
        
    if root:
        
        if isinstance(root, basestring):
            root = get_object_by_address(root)
        
        root_short_name = root.__name__.rsplit('.', 1)[-1]
            
        address_parts = address.split('.')
        heads = ['.'.join(address_parts[:i]) for i in
                 range(1, len(address_parts) + 1)]
        # heads is something like: ['garlicsim', 'garlicsim.misc',
        # 'garlicsim.misc.step_copy', 'garlicsim.misc.step_copy.StepCopy']
        
        for head in reversed(heads):
            if get_object_by_address(head) is root:
                address = address.replace(head, root_short_name, 1)
                break
                
    if shorten:
        address = shorten_address(address, root=root)
    
    return address


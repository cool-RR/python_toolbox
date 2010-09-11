import types

from garlicsim.general_misc import import_tools


def shorten_class_address(module_name, class_name):
    '''
    Shorten the address of a class.
    
    This is mostly used in `__repr__` methods of various classes to shorten the
    text and make the final output more conscise. For example, if you have a
    class `garlicsim.asynchronous_crunching.project.Project`, but which is also
    available as `garlicsim.Project`, this function will return
    'garlicsim.Project'.    
    '''
    get_module = lambda module_name: __import__(module_name, fromlist=[''])
    original_module = get_module(module_name)
    original_class = getattr(original_module, class_name)
    
    current_module_name = module_name
    
    last_successful_module_name = current_module_name
    
    while True:
        # Removing the last submodule from the module name:
        current_module_name = '.'.join(current_module_name.split('.')[:-1]) 
        
        if not current_module_name:
            # We've reached the top module and it's successful, can break now.
            break
        
        current_module = get_module(current_module_name)
        
        candidate_class = getattr(current_module, class_name, None)
        
        if candidate_class is original_class:
            last_successful_module_name = current_module_name
        else:
            break
        
    return '.'.join((last_successful_module_name, class_name))


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
    
    if not hasattr(obj, '__module__'):
        raise Exception("%s does not have a `__module__` attribute, so we "
                        "can't get it's address." % obj)
    
    if isinstance(obj, types.MethodType):
        address_candidate = '.'.join((obj.__module__, obj.im_class.__name__,
                                      obj.__name__))
        assert get_object_by_address(address_candidate) == obj
        
    else:
        address_candidate = '.'.join((obj.__module__, obj.__name__))
        assert get_object_by_address(address_candidate) is obj
    
    return address_candidate
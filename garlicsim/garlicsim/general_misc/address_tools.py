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





def get_object_from_address(address, parent_object=None):
    if not parent_object:
        if '.' not in address:
            try:
                return eval(address)
            except NameError:
                return __import__(address)   
        else: # '.' in address
            first_object_address, second_object_address = \
                address.rsplit('.', 1)
            first_object = get_object_from_address(first_object_address)
            second_object = get_object_from_address(second_object_address,
                                                    parent_object=first_object)
            return second_object
    
    else: # parent_object is not none
        
        if '.' not in address:
            
            if isinstance(parent_object, types.ModuleType) and \
               hasattr(parent_object, '__path__'):
                
                # It's a package
                import_tools.import_if_exists(
                    '.'.join((parent_object.__name__, address))
                )
                # Not keeping reference, just importing so we could get later
                
            return getattr(parent_object, address)
        
        else: # '.' in address
            first_object_address, second_object_address = \
                address.rsplit('.', 1)
            first_object = get_object_from_address(first_object_address, parent_object)
            second_object = get_object_from_address(second_object_address,
                                                    parent_object=first_object)
            return second_object
    

def get_address_from_object(obj):
    # todo: look for something like this in the community
    assert isinstance(
        obj,
        (
            type, types.FunctionType, types.ModuleType, types.MethodType
        )
    )
    
    if isinstance(obj, types.MethodType):
        address_candidate = '.'.join((obj.__module__, obj.im_class.__name__,
                                      obj.__name__))
        assert get_object_from_address(address_candidate) == obj
        
    else:
        address_candidate = '.'.join((obj.__module__, obj.__name__))
        assert get_object_from_address(address_candidate) is obj
    
    return address_candidate
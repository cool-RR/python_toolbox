import types
import re

from garlicsim.general_misc import import_tools
from garlicsim.general_misc import dict_tools
from garlicsim.general_misc import caching

# Doing at bottom:
# from .string_to_object import _get_object_by_address, resolve
from .shared import (_address_pattern, _contained_address_pattern,
                     _get_parent_and_dict_from_namespace)

# blocktododoc: add caching to some functions

# todo: when shortening, check that we're not using stuff that was excluded from
# `__all__` (if one exists)




_unresolvable_string_pattern = re.compile("<[^<>]*?'[^<>]*?'[^<>]*?>")

_address_in_unresolvable_string_pattern = re.compile("[^']*?'([^']*?)'[^']*?")


def _tail_shorten(address, root=None, namespace={}):
    '''
    '''
    if '.' not in address:
        # Nothing to shorten
        return address
    
    parent_address, child_name = address.rsplit('.', 1)
    parent = _get_object_by_address(parent_address, root=root,
                                    namespace=namespace)
    child = _get_object_by_address(address, root=root, namespace=namespace)
    
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
        
        current_parent = _get_object_by_address(current_parent_address,
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

    if not _address_pattern.match(address):
        raise ValueError("'%s' is not a legal address." % address)
        # blocktododoc change to assert
    
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


    

def _get_address(obj, shorten=False, root=None, namespace={}):
    # blocktododoc: Unprivatize since this is useful for users
    
    # todo: Support classes inside classes. Currently doesn't work because
    # Python doesn't tell us inside in which class an inner class was defined.
    # We'll probably have to do some kind of search.
    
    if not (isinstance(obj, types.ModuleType) or hasattr(obj, '__module__')):
        raise Exception("%s is not a module, nor does not have a `__module__` "
                        "attribute, therefore we can't get its address." % \
                        (obj,)) # blocktododoc: test
    
    if isinstance(obj, types.ModuleType):
        address = obj.__name__
    elif isinstance(obj, types.MethodType):
        address = '.'.join((obj.__module__, obj.im_class.__name__,
                            obj.__name__))
    else:
        address= '.'.join((obj.__module__, obj.__name__))

    try:
        object_candidate = _get_object_by_address(address)
        is_same_object = \
            (obj == object_candidate) if isinstance(obj, types.MethodType) \
            else (obj is object_candidate)
    except Exception:
        confirmed_object_address = False
    else:
        confirmed_object_address = is_same_object
        
    if not confirmed_object_address:
        # Don't try to shorten or anything, since we can't even access the
        # object.
        return address
        
    if root or namespace:
        
        if isinstance(root, basestring):
            root = _get_object_by_address(root)
            
        if isinstance(namespace, basestring):
            namespace = _get_object_by_address(namespace)


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
            

        
        address_parts = address.split('.')
        heads = ['.'.join(address_parts[:i]) for i in
                 range(1, len(address_parts) + 1)]
        # heads is something like: ['garlicsim', 'garlicsim.misc',
        # 'garlicsim.misc.step_copy', 'garlicsim.misc.step_copy.StepCopy']
        
        for head in reversed(heads):
            object_ = _get_object_by_address(head)
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

                    
    if shorten:
        address = shorten_address(address, root=root, namespace=namespace)
        
        
    if address.startswith('__builtin__.'):
        shorter_address = address.replace('__builtin__.', '', 1)
        if _get_object_by_address(shorter_address) == obj:
            address = shorter_address

            
    return address

        

    
def describe(obj, shorten=False, root=None, namespace={}):
    
    if isinstance(obj, types.ModuleType) or \
       (hasattr(obj, '__module__') and hasattr(obj, '__name__')):
        
        return _get_address(obj, shorten=shorten, root=root,
                            namespace=namespace)
    
    raw_result = repr(obj)
    current_result = raw_result
    
    ugly_reprs = []
    first_run = True
        
        
    while True:

        current_result_changed = False
        
        ugly_reprs = _unresolvable_string_pattern.findall(current_result)
        
        for ugly_repr in ugly_reprs:
            
            re_match = _address_in_unresolvable_string_pattern.match(ugly_repr)
            
            if not re_match:
                continue
            
            address_of_ugly_repr = re_match.groups()[0]
            
            try:
                object_candidate = _get_object_by_address(address_of_ugly_repr)
                # (Not using `root` and `namespace` cause it's an address
                # manufactured by `repr`.)
            except Exception:
                continue
            
            if repr(object_candidate) == ugly_repr:
                # We have a winner!
                object_winner = object_candidate
                pretty_address = _get_address(object_winner, root=root,
                                              namespace=namespace)                
                current_result = current_result.replace(ugly_repr, pretty_address)
                current_result_changed = True
          
        if current_result_changed:
            continue
        
        break
    
    return current_result
                
            
            
    
from .string_to_object import _get_object_by_address, resolve
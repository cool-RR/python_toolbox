import types
import re

from garlicsim.general_misc import import_tools
from garlicsim.general_misc import dict_tools
from garlicsim.general_misc import caching

# tododoc: split to `_get_object_by_address` and `_get_address`

# tododoc: add caching to all functions, after fixing caching with
# ArgumentsProfile to accept kwargs.

# todo: when shortening, check that we're not using stuff that was excluded from
# `__all__` (if one exists)


_address_pattern = re.compile(
    '^([a-zA-Z_][0-9a-zA-Z_]*)(\.[a-zA-Z_][0-9a-zA-Z_]*)*$'
)


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
    

def _get_address(obj, shorten=False, root=None, namespace={}):
    
    # todo: Support classes inside classes. Currently doesn't work because
    # Python doesn't tell us inside in which class an inner class was defined.
    # We'll probably have to do some kind of search.
    
    if not (isinstance(obj, types.ModuleType) or hasattr(obj, '__module__')):
        raise Exception("%s is not a module, nor does not have a `__module__` "
                        "attribute, therefore we can't get its address." % \
                        (obj,))
    
    if isinstance(obj, types.ModuleType):
        address = obj.__name__
        assert _get_object_by_address(address) is obj
    
    elif isinstance(obj, types.MethodType):
        address = '.'.join((obj.__module__, obj.im_class.__name__,
                            obj.__name__))
        assert _get_object_by_address(address) == obj
        
    else:
        address= '.'.join((obj.__module__, obj.__name__))
        assert _get_object_by_address(address) is obj
        
        
    if root or namespace:
        
        if isinstance(root, basestring):
            root = _get_object_by_address(root)
            
        if isinstance(namespace, basestring):
            namespace = _get_object_by_address(namespace)


        if namespace:
            
            if hasattr(namespace, '__getitem__') and \
               hasattr(namespace, 'keys'):
                original_namespace_dict = namespace
            else:
                original_namespace_dict = vars(namespace)

            namespace_dict = dict_tools.filter_items(
                original_namespace_dict,
                lambda key, value:
                    (getattr(value, '__name__', '').endswith(key))
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


def resolve(address, root=None, namespace={}):
    # sktechy for now    
    # tododoc: create reverse. repr won't do because it puts <> around classes
    # and stuff
    # tododoc: make sure namespace works here
    # tododoc: write tests for this
    
    # Resolving '' to None:
    if address == '':
        return None
    
    try:
        return eval(address)
    except (NameError, AttributeError):
        return _get_object_by_address(address, root, namespace)
    
    
_unresolvable_string_pattern = re.compile("<[^<>]*?'[^<>]*?'[^<>]*?>")


_address_in_unresolvable_string_pattern = re.compile("[^']*?'([^']*?)'[^']*?")

    
def describe(obj, shorten=False, root=None, namespace={}):
    #tododoc: test this
    
    if isinstance(obj, types.ModuleType) or hasattr(obj, '__module__'):
        
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
                
            
            
    
    
import re

_address_pattern = re.compile(
    "(?P<address>([a-zA-Z_][0-9a-zA-Z_]*)(\.[a-zA-Z_][0-9a-zA-Z_]*)*)"
)

def _get_parent_and_dict_from_namespace(namespace):
    
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
        
    return (parent_object, namespace_dict)
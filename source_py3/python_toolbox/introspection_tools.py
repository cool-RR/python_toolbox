# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines various introspection tools, similar to the stdlib's `inspect`.'''

from python_toolbox import cute_inspect

from python_toolbox.nifty_collections import OrderedDict


def get_default_args_dict(function):
    '''
    Get ordered dict from arguments which have a default to their default.
    
    Example:
    
        >>> def f(a, b, c=1, d='meow'): pass
        >>> get_default_args_dict(f)
        OrderedDict([('c', 1), ('d', 'meow')])
        
    '''
    arg_spec = cute_inspect.getargspec(function)
    (s_args, s_star_args, s_star_kwargs, s_defaults) = arg_spec
        
    # `getargspec` has a weird policy, when inspecting a function with no
    # defaults, to give a `defaults` of `None` instead of the more consistent
    # `()`. We fix that here:
    if s_defaults is None:
        s_defaults = ()
    
    # The number of args which have default values:
    n_defaultful_args = len(s_defaults)
    
    defaultful_args = s_args[-n_defaultful_args:] if n_defaultful_args \
                       else []
    
    return OrderedDict(zip(defaultful_args, s_defaults))
    
    
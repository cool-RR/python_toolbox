# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines several functions that may be useful when working with dicts.'''

import copy

def get_list(d, container):
    '''Get a list of the values in the dict whose keys are in `container`.'''
    return [value for (key, value) in d.iteritems() if (key in container)]

def fancy_string(d, indent=0):
    '''Show a dict as a string, slightly nicer than dict.__repr__.'''

    small_space = ' ' * indent
    
    big_space = ' ' * (indent + 4)
    
    huge_space = ' ' * (indent + 8)
    
    def show(thing, indent=0):
        space = ' ' * indent
        enter_then_space = '\n' + space
        return repr(thing).replace('\n', enter_then_space)
    
    temp1 = (
        (big_space + repr(key) + ':\n' + huge_space + show(value, indent + 8))
        for(key, value) in d.items())
    
    temp2 = small_space + '{\n' + ',\n'.join(temp1) + '\n' + small_space +'}'
    
    return temp2
    
    
    
# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines several functions that may be useful when working with
dicts.
'''

import copy

'''
def set_or_raise(dict_, key, value)
'''

'''
def deepcopy_values(d):
    new_d = d.copy()
    for key in new_d:
        new_d[key] = copy.deepcopy(new_d[key])
    return new_d
'''


def fancy_string(d, indent=0):
    '''Show a dict as a string, slightly nicer than dict.__repr__.'''
    small_space = ' ' * indent
    big_space = ' ' * (indent + 4)
    temp1 = ((big_space + str(key) + ': ' + str(value)) for (key, value) in d.items())
    temp2 = small_space + '{\n' + ',\n'.join(temp1) + '\n' + small_space +'}'
    return temp2
    
    
    
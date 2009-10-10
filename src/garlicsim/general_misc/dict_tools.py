"""
This module defines several functions that might be useful
when working with dicts.
"""

import copy

"""
def set_or_raise(dict_, key, value)
"""

def deepcopy_values(d):
    new_d = d.copy()
    for key in new_d:
        new_d[key] = copy.deepcopy(new_d[key])
    return new_d
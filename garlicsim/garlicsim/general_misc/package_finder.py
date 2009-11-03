# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines functions related to finding Python packages. See
documentation of get_packages for more info.
'''

import glob
import os
import types

def get_packages(root, include_self=False, recursive=False):
    '''
    Find all sub-packages.
    
    `root` may be a module, package, or a path.
    # todo: module? really?
    '''
    
    if isinstance(root, types.ModuleType):
        root_module = root
        root_path = os.path.dirname(root_module.__file__)
    elif isinstance(root, str):
        root_path = os.path.abspath(root)
        # Not making root_module, it might not be imported.
    
    root_module_name = os.path.split(root_path)[1]

    ######################################################
    
    result = []
    
    if include_self:
        result.append('')
        
    for entry in os.listdir(root_path):
        full_path = os.path.join(root_path, entry)
        if is_package(full_path):
            if recursive:
                result += ['.' + thing for thing in 
                           get_packages(full_path, include_self=True,
                                        recursive=True)]
            else:
                result.append('.' + entry)
    return [(root_module_name + thing) for thing in result]

def is_package(path):
    '''Is the given path a Python package?'''
    return os.path.isdir(path) and \
           glob.glob(os.path.join(path, '__init__.*'))
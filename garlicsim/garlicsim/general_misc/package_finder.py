# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines functions related to finding Python packages. See
documentation of get_packages for more info.

This module is hacky.
'''

import glob
import os
import types

def get_packages(root, include_self=False, recursive=False, self_in_name=True):
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
    
    if self_in_name:
        return [(root_module_name + thing) for thing in result]
    else:
        return result
    

def get_packages_and_modules_filenames(root, recursive=False):
    '''
    Find the filenames of all of the packages and modules inside the package.
    
    `root` may be a module, package, or a path.
    todo: module? really?
    todo: needs testing
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
        
    for entry in os.listdir(root_path):
        
        full_path = os.path.join(root_path, entry)
        
        if is_module(full_path):
            result.append(entry)
            continue
            
        elif is_package(full_path):
            result.append(entry)
            if recursive:
                inner_results = get_packages_and_modules_filenames(
                    full_path,
                    recursive=True
                )
                result += [os.path.join(entry, thing) for thing in
                           inner_results]
    
    return [os.path.join(os.path.dirname(full_path), entry) for entry in result]

def is_package(path):
    '''Is the given path a Python package?'''
    return os.path.isdir(path) and \
           glob.glob(os.path.join(path, '__init__.*'))

def is_module(path):
    '''Is the given path a Python single-file module?'''
    extension = os.path.splitext(path)[1]
    return extension.lower() in ['.py', '.pyc', '.pyo', '.pyw']


# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''
Defines functions related to finding Python packages.

See documentation of `get_module_names` for more info.

This module is hacky.
'''

import glob
import os
import types
import pkgutil

from python_toolbox import dict_tools


_extensions_by_priority = ['.pyo', '.pyc', '.pyw', '.py']
'''List of possible extenstions of Python modules, ordered by priority.'''


def get_module_names(root_path):
    '''
    Find names of all modules in a path.
    
    Supports zip-imported modules.
    '''
    
    assert isinstance(root_path, basestring)
    
    result = []
    
    for _, module_name, _ in pkgutil.iter_modules([root_path]):
        result.append('.' + module_name)
                
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
        # Not making `root_module`, it might not be imported.
    
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
    
    ### Filtering out duplicate filenames for the same module: ################
    #                                                                         #
                
    filename_to_module_name = {
        filename: os.path.splitext(filename)[0] for filename in result
    }
    module_name_to_filenames = \
        dict_tools.reverse_with_set_values(filename_to_module_name)
    
    for module_name, filenames in module_name_to_filenames.iteritems():
        if len(filenames) <= 1:
            # Does this save us from the case of packages?
            continue
        filenames_by_priority = sorted(
            filenames,
            key=lambda filename:
                _extensions_by_priority.index(os.path.splitext(filename)[1]),
        )
        redundant_filenames = filenames_by_priority[1:]
        for redundant_filename in redundant_filenames:
            result.remove(redundant_filename)
        
    #                                                                         #
    ### Done filtering duplicate filenames for the same module. ###############
    
    
    return [os.path.join(os.path.dirname(full_path), entry) for entry in
            result]


def is_package(path):
    '''Is the given path a Python package?'''
    return os.path.isdir(path) and \
           glob.glob(os.path.join(path, '__init__.*'))


def is_module(path):
    '''Is the given path a Python single-file module?'''
    extension = os.path.splitext(path)[1]
    return extension.lower() in ['.py', '.pyc', '.pyo', '.pyw']


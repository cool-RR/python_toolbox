# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines various tools related to file-system paths.'''

import sys
import os.path
import glob
import types


def list_sub_folders(path):
    '''List all the immediate sub-folders of the folder at `path`.'''
    assert os.path.isdir(path)
    files_and_folders = glob.glob(os.path.join(path, '*'))
    folders = list(filter(os.path.isdir, files_and_folders))
    return folders


def get_path_of_package(package):
    '''Get the path of a Python package, i.e. where its modules would be.'''
    path = package.__file__
    dir_path, file_name = os.path.split(path)
    assert '__init__' in file_name
    return dir_path


def get_root_path_of_module(module):
    '''
    Get the root path of a module.
    
    This is the path that should be in `sys.path` for the module to be
    importable. Note that this would give the same answer for
    `my_package.my_sub_package.my_module` as for `my_package`; it only cares
    about the root module.
    '''
    assert isinstance(module, types.ModuleType)
    module_name = module.__name__
    root_module_name = module_name.split('.', 1)[0]
    root_module = sys.modules[root_module_name]
    path_of_root_module = root_module.__file__
    dir_path, file_name = os.path.split(path_of_root_module)
    if '__init__' in file_name:
         # It's a package.
        result = os.path.abspath(os.path.join(dir_path, '..'))
    else:
        # It's a one-file module, not a package.
        result = os.path.abspath(dir_path)
    
    assert result in list(map(os.path.abspath, sys.path)) 
    return result


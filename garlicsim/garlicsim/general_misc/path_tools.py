# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines various tools related to file-system paths.'''

import sys
import os.path
import glob
import types


def list_sub_folders(path):
    '''List all the immediate sub-folders of the folder at `path`.'''
    assert os.path.isdir(path)
    files_and_folders = glob.glob(os.path.join(path, '*'))
    folders = filter(os.path.isdir, files_and_folders)
    return folders


def get_root_path_of_module(module):
    assert isinstance(module, types.ModuleType)
    module_name = module.__name__
    root_module_name = module_name.split('.', 1)[0]
    root_module = sys.modules[root_module_name]
    path_of_root_module = root_module.__file__
    dir_path, file_name = os.path.split(path_of_root_module)
    if '__init__' in file_name:
         # It's a package.
        result = os.path.normpath(os.path.join(dir_path, '..'))
    else:
        # It's a one-file module, not a package.
        result = dir_path
    assert result in sys.path
    return result

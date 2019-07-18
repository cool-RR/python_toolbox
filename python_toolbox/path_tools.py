# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines various tools related to file-system paths.'''

import sys
import os
import pathlib

import glob
import types

_is_windows = (os.name == 'nt')
null_path = pathlib.Path(os.path.devnull)
path_type = pathlib.WindowsPath if _is_windows else pathlib.PosixPath

def list_sub_folders(path):
    '''List all the immediate sub-folders of the folder at `path`.'''
    path = pathlib.Path(path)
    assert path.is_dir()
    return tuple(filter(pathlib.Path.is_dir, path.glob('*')))


def get_path_of_package(package):
    '''Get the path of a Python package, i.e. where its modules would be.'''
    path = pathlib.Path(package.__file__)
    assert '__init__' in path.name
    return path.parent


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
    path_of_root_module = pathlib.Path(root_module.__file__)
    if '__init__' in path_of_root_module.name:
         # It's a package.
        result = path_of_root_module.parent.parent.absolute()
    else:
        # It's a one-file module, not a package.
        result = path_of_root_module.parent.absolute()

    assert result in list(map(pathlib.Path.absolute,
                              map(pathlib.Path, sys.path)))
    return result



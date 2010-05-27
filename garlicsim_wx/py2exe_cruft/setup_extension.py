# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Module for packaging garlicsim_wx as executable using py2exe.

Normally the contents of this module would be in setup.py; But py2exe introduces
so much cruft, and I wanted to keep it away from my setup.py. So setup.py
imports this module when it gets a `py2exe` command. This module should not be
used otherwise.

This module assumes that the `garlicsim` and `garlicsim_lib` folders are
alongside the `garlicsim_wx` folder, as in the official git repo of GarlicSim.
'''

import setuptools
import py2exe
import imp
import sys, os.path, glob
import pkgutil

# This module is meant to be imported from the garlicsim_wx setup.py file, and
# should not be used otherwise:
assert any('setup.py' in s for s in sys.argv)

path_to_garlicsim = os.path.abspath('../garlicsim')
path_to_garlicsim_lib = os.path.abspath('../garlicsim_lib')
paths_to_add = [path_to_garlicsim, path_to_garlicsim_lib]
for path_to_add in paths_to_add:
    if path_to_add not in sys.path:
        sys.path.append(path_to_add)

def cute_find_module(module_name):
    '''Find the path to a module by its name.'''
    current_module_name = module_name
    current_paths = sys.path

    while '.' in current_module_name:
        (big_package_name, current_module_name) = \
            current_module_name.split('.', 1)
        big_package_path = imp.find_module(big_package_name, current_paths)[1]
        current_paths = [big_package_path]
    
    return imp.find_module(current_module_name, current_paths)[1]
    

def package_to_path(package):
    '''
    Given a package name, convert to path.
    
    The path will be relative to the folder that contains the root package.
    
    Example:
    package_to_path('numpy.core') == 'numpy/core'
    '''
    return package.replace('.', '/')


def get_garlicsim_packages():
    '''
    Get all the packages in garlicsim.
    
    This returns an answer in the form: ['garlicsim.data_structures',
    'garlicsim.bootstrap', 'garlicsim.misc', ...]
    '''
    return ['garlicsim.' + p for p
            in setuptools.find_packages('../garlicsim/garlicsim')] + \
           ['garlicsim']

garlicsim_packages = get_garlicsim_packages()


def get_garlicsim_lib_packages():
    '''
    Get all the packages in garlicsim_lib.
    
    This returns an answer in the form: ['garlicsim_lib.simpacks.life',
    'garlicsim_lib.simpacks.prisoner', ...]
    '''
    return ['garlicsim_lib.' + p for p
            in setuptools.find_packages('../garlicsim_lib/garlicsim_lib')] + \
           ['garlicsim_lib']

garlicsim_lib_packages = get_garlicsim_lib_packages()


def get_garlicsim_wx_packages():
    '''
    Get all the packages in garlicsim_wx.
    
    This returns an answer in the form: ['garlicsim_wx.frame',
    'garlicsim_wx.widgets', 'garlicsim_wx.misc', ...]
    '''
    return ['garlicsim_wx.' + p for p
            in setuptools.find_packages('garlicsim_wx')] + \
           ['garlicsim_wx']

garlicsim_wx_packages = get_garlicsim_wx_packages()


def get_garlicsim_data_files():
    '''
    Get garlicsim's data files.
    
    This returns a list of tuples, where the second item in each tuple is a list
    of files and the first item is the path to which these files should be
    copied when doing the py2exe packaging.
    '''
    total_data_files = []
    for package in garlicsim_packages:
        path = package_to_path(package)
        all_files_and_folders = \
            glob.glob(path_to_garlicsim + '/' + path + '/*')
        data_files = [f for f in all_files_and_folders if
                      (not '.py' in f[-4:]) and (not os.path.isdir(f))]
        total_data_files.append(('lib/' + path, data_files))
    return total_data_files


def get_garlicsim_lib_data_files():
    '''
    Get garlicsim_lib's data files.
    
    This returns a list of tuples, where the second item in each tuple is a list
    of files and the first item is the path to which these files should be
    copied when doing the py2exe packaging.
    '''
    total_data_files = []
    for package in garlicsim_lib_packages:
        path = package_to_path(package)
        all_files_and_folders = \
            glob.glob(path_to_garlicsim_lib + '/' + path + '/*')
        data_files = [f for f in all_files_and_folders if
                      (not '.py' in f[-4:]) and (not os.path.isdir(f))]
        total_data_files.append(('lib/' + path, data_files))
    return total_data_files


def get_garlicsim_wx_data_files():
    '''
    Get garlicsim_wx's data files.
    
    This returns a list of tuples, where the second item in each tuple is a list
    of files and the first item is the path to which these files should be
    copied when doing the py2exe packaging.
    '''
    total_data_files = []
    for package in garlicsim_wx_packages:
        path = package_to_path(package)
        all_files_and_folders = glob.glob(path + '/*')
        data_files = [f for f in all_files_and_folders if
                      (not '.py' in f[-4:]) and (not os.path.isdir(f))]
        total_data_files.append(('lib/' + path, data_files))
    return total_data_files

def get_garlicsim_script_files():
    '''
    Get garlicsim's script files.
    
    This returns a list of tuples, where the second item in each tuple is a list
    of files and the first item is the path to which these files should be
    copied when doing the py2exe packaging.
    '''
    total_script_files = []
    garlicsim_script_packages = \
        [p for p in garlicsim_packages if 'garlicsim.scripts' in p]
    for package in garlicsim_script_packages:
        path = package_to_path(package)
        all_files_and_folders = \
            glob.glob(path_to_garlicsim + '/' + path + '/*')
        py_files = [f for f in all_files_and_folders if
                    ('.py' == f[-3:]) and (not os.path.isdir(f))]
        total_script_files.append(('lib/' + path, py_files))
    return total_script_files


def get_dlls_and_stuff():
    '''
    Get some miscellaneous files that need to be copied to py2exe_dist.
    
    This returns a list of tuples, where the second item in each tuple is a list
    of files and the first item is the path to which these files should be
    copied when doing the py2exe packaging.
    '''
    total_data_files = []
    path_to_folder = './py2exe_cruft/dlls_and_stuff'
    folders_to_do = [path_to_folder]
    while folders_to_do:
        path = folders_to_do.pop()
        assert not os.path.isabs(path)
        all_files_and_folders = glob.glob(path + '/*')
        files = [f for f in all_files_and_folders if (not os.path.isdir(f))]
        folders = [f for f in all_files_and_folders if os.path.isdir(f)]
        folders_to_do += folders
        total_data_files.append(
            (
                os.path.relpath(path, './py2exe_cruft/dlls_and_stuff'),
                files
            )
        )
    return total_data_files


def get_all_data_files():
    '''
    Get all the data files that need to be copied to py2exe_dist.
    
    This includes the data files for the `garlicsim`, `garlicsim_lib` and
    `garlicsim_wx` packages, and some miscellaneous data files.
    
    This returns a list of tuples, where the second item in each tuple is a list
    of files and the first item is the path to which these files should be
    copied when doing the py2exe packaging.
    '''
    return get_garlicsim_data_files() + get_garlicsim_lib_data_files() + \
           get_garlicsim_wx_data_files() + get_garlicsim_script_files() + \
           get_dlls_and_stuff()


def get_all_submodules(package_name):
    '''
    Get all submodules of a package, recursively.
    
    This includes both modules and packages.
    
    Example:
    
    get_all_subpackages('numpy') == ['numpy.compat._inspect',
    'numpy.compat.setup', 'numpy.compat.setupscons', ... ]
    '''
    package_path = cute_find_module(package_name)
    
    subpackage_names = [(package_name + '.' + m) for m in 
                        setuptools.find_packages(package_path)]
    
    modules = []
    for subpackage_name in subpackage_names:
        subpackage_path = cute_find_module(subpackage_name)
        modules += [
            module for (loader, module, is_package) in 
            pkgutil.iter_modules([subpackage_path], subpackage_name + '.')
            if not is_package
        ]
        modules.append(subpackage_name)    
        
    return modules


# This is a list of packages that should be included in the library, with all
# their submodules. In theory, the `packages` option of py2exe should take care
# of it, but it has bugs in it so we're doing this ourselves.
packages_to_include_with_all_submodules = [
    
    'garlicsim', 'garlicsim_lib',
    
    'numpy', 'scipy'
    
]


# List of modules to be included in the library.
includes = reduce(
    list.__add__,
    [get_all_submodules(package_name) for package_name in \
     packages_to_include_with_all_submodules]
)


py2exe_kwargs = {
    
    # We're giving a less nerdy description here, because this will be shown on
    # the executable, where non-nerds might see it:
    'description': 'Pythonic framework for computer simulations',
    
    'windows': [
        {
            'script': 'py2exe_cruft/GarlicSim.py',
            'icon_resources': [
                (
                    0,
                    'garlicsim_wx/misc/icon_bundle/images/garlicsim.ico'
                )
            ]
        }
        ],
    'data_files': get_all_data_files(),
    
    # We don't really have a zipfile, this is the path to the library folder:
    'zipfile': 'lib/library.zip',
    # Keep in mind that this `library.zip` filename here will simply be ignored.
    
    'options': {
        'py2exe': {
            'dist_dir': 'py2exe_dist',
            
            # We prefer to have all the files in a folder instead of a zip file.
            'skip_archive': True,
            
            'includes': includes,
            
            'dll_excludes': ['UxTheme.dll'],
            
        }
    }
}
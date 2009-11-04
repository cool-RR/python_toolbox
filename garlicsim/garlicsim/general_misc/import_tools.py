# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines various tools related to importing.
'''

import os.path
import imp
from garlicsim.general_misc import package_finder

def import_by_path(path, name=None):
    '''
    Import module/package by path.
    
    You may specify a name: This is helpful only if it's an hierarchical name,
    i.e. a name with dots like "orange.claw.hammer". This will become the
    imported module's __name__ attribute. Otherwise only the short name,
    "hammer", will be used, which might cause problems in some cases. (Like
    when using multiprocessing.
    '''
    short_name = os.path.splitext(os.path.split(path)[1])[0]
    if name is None: name = short_name
    path_to_dir = os.path.dirname(path)
    my_file = None
    try:
        (my_file, pathname, description) = \
            imp.find_module(short_name, [path_to_dir])
        module = imp.load_module(name, my_file, pathname, description)
    finally:
        if my_file is not None:
            my_file.close()
        
    return module
    

def import_all(package, exclude='__init__'):
    '''
    Import all the modules and packages that live inside the given package.
    
    This is not recursive. Modules and packages defined inside a subpackage
    will not be imported (of course, that subpackage itself may import them
    anyway.)
    
    You may specify a module/package to exclude, which is by default
    `__init__`.
    
    Returns a list with all the imported modules and packages.
    
    todo: only tested with __init__ passed in
    '''
    
    paths = package_finder.get_packages_and_modules_filenames(package)
    
    names = {}
    for path in paths:
        name = os.path.splitext(os.path.split(path)[1])[0]
        if name == exclude:
            continue
        full_name = package.__name__ + '.' + name
        names[path] = full_name
        
    d = {}
    
    for (path, name) in names.items():
        d[name] = import_by_path(path, name)
    
    return d
        
    
    
        
    
    
    


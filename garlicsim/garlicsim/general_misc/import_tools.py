# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines various tools related to importing.'''

import sys
import os.path
import imp

from garlicsim.general_misc import package_finder
from garlicsim.general_misc import caching


def import_by_path(path, name=None):
    '''
    Import module/package by path.
    
    You may specify a name: This is helpful only if it's an hierarchical name,
    i.e. a name with dots like "orange.claw.hammer". This will become the
    imported module's __name__ attribute. Otherwise only the short name,
    "hammer", will be used, which might cause problems in some cases. (Like
    when using multiprocessing.)
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
    

def import_all(package, exclude='__init__', silent_fail=False):
    '''
    Import all the modules and packages that live inside the given package.
    
    This is not recursive. Modules and packages defined inside a subpackage
    will not be imported. (Of course, that subpackage itself may import them
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
        try:
            module = import_by_path(path, name)
        except Exception:
            if not silent_fail:
                raise
        d[name] = module
        short_module_name = name.rsplit('.', 1)[-1]
        if not hasattr(package, short_module_name):
            setattr(package, short_module_name, module)
    
    return d


def normal_import(module_name):
    if '.' in module_name:
        package_name, submodule_name = module_name.rsplit('.', 1)
        package = __import__(module_name)
        return reduce(getattr, [package] + module_name.split('.')[1:])
    else:
        return __import__(module_name)
    

@caching.cache() # todo: clear cache if sys.path changes
def import_if_exists(module_name, silent_fail=False):
    '''
    Import module by name and return it, only if it exists.
    
    If `silent_fail` is True, will return None if the module doesn't exist. If
    `silent_fail` is False, will raise ImportError.
    '''    
    if '.' in module_name:
        package_name, submodule_name = module_name.rsplit('.', 1)
        package = import_if_exists(package_name, silent_fail=silent_fail)
        if not package:
            assert silent_fail is True
            return None
        package_path = package.__path__
        try:
            imp.find_module(submodule_name, package_path)
        except ImportError:
            if silent_fail is True:
                return None
            else: # silent_fail is False
                raise
    else: # '.' not in module_name
        try:
            imp.find_module(module_name)
        except ImportError:
            if silent_fail is True:
                return None
            else: # silent_fail is False
                raise

    # Not actually using the result of `imp.find_module`, just want to know that
    # it worked and the module exists. We'll let the conventional `__import__`
    # find the module again, assuming its finding procedure will work exactly
    # the same as imp's.
        
    return normal_import(module_name)
    
    
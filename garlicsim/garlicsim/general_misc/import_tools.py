# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines various tools related to importing.'''

import sys
import os.path
import imp
import zipimport

from garlicsim.general_misc import package_finder
from garlicsim.general_misc import caching

    

def import_all(package, exclude='__init__', silent_fail=False):
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
        try:
            d[name] = normal_import(name)
        except Exception:
            if not silent_fail:
                raise
    
    return d


def normal_import(module_name):
    '''
    Import a module.
    
    This function has several advantages over `__import__`:
    
     1. It avoids the weird `fromlist=['']` that you need to give `__import__`
        in order for it to return the specific module you requested instead of 
        the outermost package, and
    
     2. It avoids a weird bug in Linux, where importing using `__import__` can
        lead to a `module.__name__` containing two consecutive dots.
        
    '''
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
    
    If `silent_fail` is `True`, will return `None` if the module doesn't exist.
    If `silent_fail` is False, will raise `ImportError`.
    
    `silent_fail` applies only to whether the module exists or not; If it does
    exist, but there's an error importing it... *release the hounds.*
    
    I mean, we just raise the error.
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

    # Not actually using the result of `imp.find_module`, just want to know
    # that it worked and the module exists. We'll let `normal_import` find the
    # module again, assuming its finding procedure will work exactly the same
    # as `imp`'s.
        
    return normal_import(module_name)


def _module_exists_in_some_zip_path(module_name):
    '''
    Return whether a module by the name `module_name` exists in a zip archive.
    
    Used internally by `exists`.
    '''
    assert '.' not in module_name
    
    zip_paths = [path for path in sys.path if '.zip' in path]
    # todo: Find better way to filter zip paths.
    
    for zip_path in zip_paths:

        # Trying to create a zip importer:
        try:
            zip_importer = zipimport.zipimporter(zip_path)
        except zipimport.ZipImportError:
            continue
            # Excepted `ZipImportError` because we may have zip paths in
            # `sys.path` that don't really exist, which causes `zipimport` to
            # raise `ZipImportError`.
            #
            # todo: should find smarter way of catching this, excepting
            # `ZipImportError` is not a good idea.
        
        if zip_importer.find_module(module_name) is not None:    
            return True
        else:
            continue
        
    return False


def exists(module_name):
    '''
    Return whether a module by the name `module_name` exists.
    
    This seems to be the best way to carefully import a module.
    
    Currently implemented for top-level packages only. (i.e. no dots.)
    
    Supports modules imported from a zip file.
    '''
    assert '.' not in module_name
    try:
        imp.find_module(module_name)
    except ImportError:
        return _module_exists_in_some_zip_path(module_name)
    else:
        return True

    
# Unused for now:

#def import_by_path(path, name=None):
    #'''
    #Import module/package by path.
    
    #You may specify a name: This is helpful only if it's an hierarchical name,
    #i.e. a name with dots like "orange.claw.hammer". This will become the
    #imported module's __name__ attribute. Otherwise only the short name,
    #"hammer", will be used, which might cause problems in some cases. (Like
    #when using multiprocessing.)
    #'''
    #short_name = os.path.splitext(os.path.split(path)[1])[0]
    #if name is None: name = short_name
    #path_to_dir = os.path.dirname(path)
    #my_file = None
    #try:
        #(my_file, pathname, description) = \
            #imp.find_module(short_name, [path_to_dir])
        #module = imp.load_module(name, my_file, pathname, description)
    #finally:
        #if my_file is not None:
            #my_file.close()
        
    #return module
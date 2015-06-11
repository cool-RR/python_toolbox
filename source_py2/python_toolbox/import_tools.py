# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines various tools related to importing.'''

import sys
import os.path
import imp
import zipimport
try:
    import pathlib
except:
    from python_toolbox.third_party import pathlib


from python_toolbox import package_finder
from python_toolbox import caching

    

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
        name = path.stem
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
    

@caching.cache() # todo: clear cache if `sys.path` changes
def import_if_exists(module_name, silent_fail=False):
    '''
    Import module by name and return it, only if it exists.
    
    If `silent_fail` is `True`, will return `None` if the module doesn't exist.
    If `silent_fail` is False, will raise `ImportError`.
    
    `silent_fail` applies only to whether the module exists or not; if it does
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
        if not exists(submodule_name, package_path):
            if silent_fail is True:
                return None
            else: # silent_fail is False
                raise ImportError("Can't find %s." % module_name)
    else: # '.' not in module_name
        if not exists(module_name):
            if silent_fail is True:
                return None
            else: # silent_fail is False
                raise ImportError("Can't find %s." % module_name)

    return normal_import(module_name)


def exists(module_name, path=None):
    '''
    Return whether a module by the name `module_name` exists.
    
    This seems to be the best way to carefully import a module.
    
    Currently implemented for top-level packages only. (i.e. no dots.)
    
    Supports modules imported from a zip file.
    '''
    if '.' in module_name:
        raise NotImplementedError
    module_file = None
    try:
        module_file, _, _ = find_module(module_name, path=path,
                                        legacy_output=True)
    except ImportError:
        return False
    else:
        return True
    finally:
        if hasattr(module_file, 'close'):
            module_file.close()
        

def _import_by_path_from_zip(path):
    '''Import a module from a path inside a zip file.'''
    assert '.zip' in path
    
    parent_path, child_name = path.rsplit(os.path.sep, 1)
    zip_importer = zipimport.zipimporter(parent_path)
    module = zip_importer.load_module(child_name)
        
    return module

    
def import_by_path(path, name=None, keep_in_sys_modules=True):
    '''
    Import module/package by path.
    
    You may specify a name: This is helpful only if it's an hierarchical name,
    i.e. a name with dots like "orange.claw.hammer". This will become the
    imported module's __name__ attribute. Otherwise only the short name,
    "hammer", will be used, which might cause problems in some cases. (Like
    when using multiprocessing.)
    '''
    path = pathlib.Path(path)
    if '.zip' in path:
        if name is not None:
            raise NotImplementedError
        module = _import_by_path_from_zip(path)
        
    else: # '.zip' not in path
        short_name = path.stem
        
        if name is None: name = short_name
        my_file = None
        try:
            (my_file, pathname, description) = \
                imp.find_module(short_name, [path.parent])
            module = imp.load_module(name, my_file, pathname, description)
        finally:
            if my_file is not None:
                my_file.close()
                
    if not keep_in_sys_modules:
        del sys.modules[module.__name__]
        
    return module


def find_module(module_name, path=None, look_in_zip=True, legacy_output=False):
    '''
    Search for a module by name and return its filename.
    
    When `path=None`, search for a built-in, frozen or special module and
    continue search in `sys.path`.
    
    When `legacy_output=True`, instead of returning the module's filename,
    returns a tuple `(file, filename, (suffix, mode, type))`.
    
    When `look_in_zip=True`, also looks in zipmodules.
    
    todo: Gives funky output when `legacy_output=True and look_in_zip=True`.
    '''
    # todo: test
    if look_in_zip:
        try:
            result = _find_module_in_some_zip_path(module_name, path)
        except ImportError:
            pass
        else:
            return (None, result, None) if legacy_output else result
            
    
    if '.' in module_name:
        parent_name, child_name = module_name.rsplit('.', 1)
        parent_path = find_module(parent_name, path)
        result = imp.find_module(child_name, [parent_path])
    else:
        result = imp.find_module(module_name, path)
        
    if legacy_output:
        return result
    else: # legacy_output is False
        file_, path_, description_ = result
        if file_ is not None:
            file_.close()
        return path_

    
def _find_module_in_some_zip_path(module_name, path=None):
    '''
    If a module called `module_name` exists in a zip archive, get its path.
    
    If the module is not found, raises `ImportError`.
    '''
    original_path_argument = path
    
    if path is not None:
        zip_paths = path
    else:
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
        
        result = zip_importer.find_module(
            # Python's zip importer stupidly needs us to replace dots with path
            # separators:  
            _module_address_to_partial_path(module_name)
        )
        if result is None:
            continue
        else:
            assert result is zip_importer
            
            #if '.' in module_name:
                #parent_package_name, child_module_name = \
                    #module_name.rsplit('.')
                #leading_path = \
                    #_module_address_to_partial_path(parent_package_name)
            #else:
                #leading_path = ''
                
            return pathlib.Path(str(zip_path)) / \
                                   _module_address_to_partial_path(module_name)

    if original_path_argument is not None:
        raise ImportError('Module not found in the given zip path.')
    else:
        raise ImportError('Module not found in any of the zip paths.')

    
def _module_address_to_partial_path(module_address):
    '''
    Convert a dot-seperated address to a path-seperated address.
    
    For example, on Linux, `'python_toolbox.caching.cached_property'` would be
    converted to `'python_toolbox/caching/cached_property'`.
    '''
    return os.path.sep.join(module_address.split('.'))
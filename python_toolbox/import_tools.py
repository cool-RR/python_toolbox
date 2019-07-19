# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines various tools related to importing.'''

import sys
import os.path
import importlib
import zipimport
import functools
import pathlib


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
        return functools.reduce(getattr,
                                [package] + module_name.split('.')[1:])
    else:
        return __import__(module_name)


def import_if_exists(module_name):
    '''
    Import module by name and return it, only if it exists.
    '''
    try:
        return __import__(module_name)
    except ModuleNotFoundError:
        return None


def exists(module_name, package_name=None):
    '''
    Return whether a module by the name `module_name` exists.

    This seems to be the best way to carefully import a module.

    Currently implemented for top-level packages only. (i.e. no dots.)

    Supports modules imported from a zip file.
    '''
    if '.' in module_name:
        raise NotImplementedError
    return bool(importlib.util.find_spec(module_name, package_name))


def _module_address_to_partial_path(module_address):
    '''
    Convert a dot-seperated address to a path-seperated address.

    For example, on Linux, `'python_toolbox.caching.cached_property'` would be
    converted to `'python_toolbox/caching/cached_property'`.
    '''
    return os.path.sep.join(module_address.split('.'))
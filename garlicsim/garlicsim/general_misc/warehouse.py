# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module lets you import things dynamically from a warehouse. See
documentation of `create` for more information about what a warehouse is.

todo: maybe class instead of func?
todo: make WarehouseError and fuck assert
'''

import os
import warnings

from . import import_tools

__all__ = ['create']


class WarehouseError(Exception):
    '''Error to raise when there is a warehouse-related error.'''

def create(package):
    '''
    Get all objects defined in modules/packages that live in a warehouse.
    
    What is a warehouse? A warehouse is a package that has within it modules
    and packages, and it uses this function to automatically retrieve all the
    objects from all these modules and packages, and get them in one list.
    
    What is it good for? In the GarlicSim project, there is a warehouse called
    crunchers_warehouse. Inside it there are various modules that define
    different types of "crunchers". One is a module cruncher_thread, which
    defines CruncherThread, another is a module cruncher_process, which
    defines CruncherProcess. The warehouse uses this function to keep a list of
    all these crunchers. If one day there will be added a module that defines
    CruncherWhatever, and it will be added to the warehouse, the list will
    automatically include it. This makes it very frictionless to add/remove
    crunchers in the warehouse.
    
    How to use this function? This way works, written in the warehouse's
    __init__:
    
    import sys
    from ...wherever import warehouse
    this_module = sys.modules[__name__]
    objects = warehouse.create(this_module)
    
    That's it. Assuming the package's name is `my_package`, the list of objects
    will now be available as `my_package.objects`.
    
    
    todo: works when frozen?
    '''
    
    things = {}
    modules = import_tools.import_all(package)
    for (module_name, module) in modules.items():
        if not hasattr(module, '__all__'):
            raise WarehouseError('''Module in warehouse must define __all__ \
which declares exactly which objects should be collected.''')
        for name in module.__all__:
            if name in things:
                raise WarehouseError('''Duplicity in warehouse: the name %s \
is defined in two different modules: %s and %s.''' % \
                    (name, things[name].__module__, module.__name__))
            things[name] = getattr(module, name)
        
    return things

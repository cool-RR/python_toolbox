# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''
A bootstrap module for `python_toolbox`.

It checks all prerequisites are installed.
'''

import sys

### Confirming correct Python version: ########################################
#                                                                             #
if sys.version_info[0] >= 3:
    raise Exception("Python 3.x is not supported, only Python 2.6 and Python "
                    "2.7.")
if sys.version_info[1] <= 4:
    raise Exception(
        "You're using Python <= 2.5, but this package requires either Python "
        "2.6 or Python 2.7, so you can't use it unless you upgrade your "
        "Python version."
    )
#                                                                             #
### Finished confirming correct Python version. ###############################


frozen = getattr(sys, 'frozen', None)
is_pypy = ('__pypy__' in sys.builtin_module_names)


def __check_prerequisites():
    '''
    Check that all modules required for `python_toolbox` are installed.
    
    Returns a list of some imported modules: A reference to this list should be
    kept alive so to prevent the imported modules from being garbage-collected,
    which would cause Python to load them twice, which would needlessly
    increase startup time.
    '''
    
    modules = []
    
    class MissingModule(Exception):
        '''A required module is not found.'''
    
    def check_pkg_resources():
        try:
            import pkg_resources
        except ImportError:
            raise MissingModule(
                "`pkg_resources` is required, but it's not currently "
                "installed on your system. It comes with `distribute`, so "
                "please install it according to the instructions here: "
                "http://pypi.python.org/pypi/distribute"
            )
        else:
            return [pkg_resources]
    
    def check_distribute():
        if frozen:
            # Can't check that `distribute` is installed when frozen with
            # `py2exe`.
            return []
        import pkg_resources
        try:
            pkg_resources.require('distribute')
        except pkg_resources.DistributionNotFound:
            raise MissingModule(
                "`distribute` is required, but it's not currently installed "
                "on your system. Please install it according to the "
                "instructions here: http://pypi.python.org/pypi/distribute"
            )
        else:
            # Returning empty list because we didn't import `distribute`:
            return []
        
        
    checkers = [check_pkg_resources, check_distribute]
    
    for checker in checkers:
        modules += checker()
    
    return modules


__modules_list = __check_prerequisites()

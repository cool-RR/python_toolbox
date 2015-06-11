# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''
Defines the `troubleshoot_pstats` function.

See its documentation for more details.
'''

import os

from python_toolbox import import_tools


def troubleshoot_pstats():
    '''
    Let the user know if there might be an error importing `pstats`.
    
    Raises an exception if it thinks it caught the problem. So if this function
    didn't raise an exception, it means it didn't manage to diagnose the
    problem.
    '''    
    if not import_tools.exists('pstats') and os.name == 'posix':
        
        raise ImportError(
            "The required `pstats` Python module is not installed on your "
            "computer. Since you are using Linux, it's possible that this is "
            "because some Linux distributions don't include `pstats` by "
            "default. You should be able to fix this by installing the "
            "`python-profiler` package in your OS's package manager. "
            "(Possibly you will have to get this package from the multiverse.)"
        )
    
        
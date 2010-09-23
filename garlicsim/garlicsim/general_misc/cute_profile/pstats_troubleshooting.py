import os

from garlicsim.general_misc import import_tools


def troubleshoot_pstats():
    '''
    
    Raises an exception if it thinks it caught the problem. So if this function
    didn't raise an exception, it means it didn't manage to diagnose the
    problem.
    '''    
    if import_tools.import_if_exists('pstats', silent_fail=True) is None and \
       os.name == 'posix':
        
        raise ImportError(
            "The required `pstats` Python module is not installed on your "
            "computer. Since you are using Linux, it's possible that this is "
            "because some Linux distributions don't include `pstats` by "
            "default. You should be able to fix this by installing the "
            "`python-profiler` package in your OS's package manager. "
            "(Possibly you will have to get this package from the multiverse.)"
        )
    
        
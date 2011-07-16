# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
A bootstrap module for garlicsim.

It checks all prerequisites are installed.
'''

import sys

### Confirming correct Python version: ########################################
#                                                                             #
if sys.version_info[0] >= 3:
    raise Exception('This package is not compatible with Python 3.x. Use '
                    '`garlicsim_py3` instead.')
if sys.version_info[1] <= 4:
    raise Exception('This package requires Python 2.5 and upwards. (Not '
                    'including 3.x).')
#                                                                             #
### Finished confirming correct Python version. ###############################


frozen = getattr(sys, 'frozen', None)


def __check_prerequisites():
    '''
    Check that all modules required for `garlicsim` are installed.
    
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
            raise MissingModule("`pkg_resources` is required, but it's not "
                                "currently installed on your system. It comes "
                                "with `distribute`, so please install it "
                                "according to the instructions here: "
                                "http://pypi.python.org/pypi/distribute")
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
            raise MissingModule("`distribute` is required, but it's not "
                                "currently installed on your system. Please "
                                "install it according to the instructions "
                                "here: http://pypi.python.org/pypi/distribute")
        else:
            # Returning empty list because we didn't import `distribute`:
            return []
        
    def check_pywin32():
        if not sys.platform == 'win32':
            return []
        try:
            import win32api
            import win32process
            import win32com
        except ImportError:
            raise MissingModule(
                "`pywin32` is required, but it's not currently installed on "
                "your system. Please install it according to the instructions "
                "here: http://sourceforge.net/projects/pywin32/files/pywin32/"
            )
        else: 
            return [win32api, win32process, win32com]
        
        
    checkers = [check_pkg_resources, check_distribute, check_pywin32]
    
    for checker in checkers:
        modules += checker()
    
    return modules


def __check_problematic_psyco_version():
    if 'psyco' in sys.modules:
        psyco = sys.modules['psyco']
        if psyco.version_info[0] >= 2:
            import warnings
            warnings.warn("You seem to have Psyco version 2 (or newer) "
                          "installed. It might conflict with `garlicsim`, so "
                          "you may want to avoid using it. Psyco version 1.6 "
                          "is fine and recommended.")

__modules_list = __check_prerequisites()

__check_problematic_psyco_version()


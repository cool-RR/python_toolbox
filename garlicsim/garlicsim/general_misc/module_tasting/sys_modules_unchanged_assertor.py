# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `SysModulesAssertor` class.

See its documentation for more information.
'''

import sys
from garlicsim.general_misc import context_managers


known_false_positive_new_modules = set([
    'garlicsim.general_misc.zlib'
])


class SysModulesUnchangedAssertor(context_managers.ContextManager):
    '''
    Context manager that asserts that `sys.modules` wasn't changed in suite.
    
    Some exceptions are made in `known_false_positive_new_modules`. These
    modules are allowed to appear in `sys.modules`.
    '''
    
    def __enter__(self):
        self.old_sys_modules = sys.modules.copy()

        
    def __exit__(self, exc_type, exc_value, exc_traceback):
        new_modules_in_sys_modules = [module_name for module_name in
                                      sys.modules if module_name not in
                                      self.old_sys_modules]
        assert set(new_modules_in_sys_modules).issubset(
            known_false_positive_new_modules
        )



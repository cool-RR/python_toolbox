# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `SysModulesAssertor` class.

See its documentation for more information.
'''

import sys
from garlicsim.general_misc import context_manager


_known_false_positive_new_modules = set([
    'garlicsim.general_misc.zlib'
])


class SysModulesUnchangedAssertor(context_manager.ContextManager):
    def __enter__(self):
        self.old_sys_modules = sys.modules.copy()
    
    def __exit__(self, exc_type, exc_value, traceback):
        new_modules_in_sys_modules = [module_name for module_name in
                                      sys.modules if module_name not in
                                      self.old_sys_modules]
        assert set(new_modules_in_sys_modules).issubset(
            _known_false_positive_new_modules
        )






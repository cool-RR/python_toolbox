# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `` class.

See its documentation for more information.
'''

from __future__ import with_statement

import os.path
import sys

import nose

from garlicsim.general_misc import module_tasting
from garlicsim.general_misc import temp_file_tools
from garlicsim.general_misc import cute_iter_tools
from garlicsim.general_misc import sys_tools

from . import sample_package_creation


module_names = ['my_package', 'my_package.__init__', 'my_package.johnny']

is_python_25 = (sys.version_info[:2] == (2, 5))


def test_module_tasting():
    
    combinations = cute_iter_tools.product(
        sample_package_creation.formats,
        module_names
    )
    
    for format, module_name in combinations:
        yield _check_module_tasting, format, module_name
    
    

def _check_module_tasting(format, module_name):
    
    if format == 'zip' and is_python_25:
        raise nose.SkipTest("Python 2.5 can't handle module-tasting of "
                            "zip-imported modules.")
    
    old_sys_modules = sys.modules.copy()
    
    with temp_file_tools.TemporaryFolder(prefix='temp_garlicsim_') as \
                                                              temporary_folder:
        
    
        path_to_add = sample_package_creation.create_sample_package(
            format,
            temporary_folder
        )
        
        with sys_tools.TempSysPathAdder(path_to_add):
            
            tasted_module = module_tasting.taste_module(module_name)
            
            if module_name in ('my_package', 'my_package.__init__'):
                assert tasted_module.__doc__ == \
                    "The tasted module's docstring."
                assert tasted_module.my_string == \
                    'Just a string'
                assert tasted_module.my_list == \
                    ['A', 'list', 'of', 'stuff']
                
            else:
                assert module_name == 'my_package.johnny'
                assert tasted_module.number_nine == 9
                
    
    ### Ensuring the module wasn't added to `sys.modules`: ####################
    #                                                                         #
    new_module_names = [key for key in sys.modules if key
                        not in old_sys_modules]
    for new_module_name in new_module_names:
        assert not new_module_name.startswith(module_name)
    #                                                                         #
    ### Finished ensuring the module wasn't added to `sys.modules`. ###########



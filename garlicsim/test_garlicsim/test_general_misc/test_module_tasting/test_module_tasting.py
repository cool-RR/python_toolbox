# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `` class.

See its documentation for more information.
'''

import os.path
import sys

from garlicsim.general_misc import module_tasting

def test_module_tasting():
    old_sys_modules = sys.modules.copy()
    path = os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            'sample_modules/x/__init__.py'
        )
    )
    
    module_address = ('test_garlicsim.test_general_misc.test_module_tasting.'
                      'sample_modules.x')
    
    tasted_module = module_tasting.taste_module(
        #path
        ('test_garlicsim.test_general_misc.test_module_tasting.'
         'sample_modules.x')
    )
    assert tasted_module.__doc__ == "The tasted module's docstring."
    assert tasted_module.my_string == 'Just a string'
    assert tasted_module.my_list == ['A', 'list', 'of', 'stuff']

    ### Ensuring the module wasn't added to `sys.modules`: ####################
    #                                                                         #
    new_module_names = [key for key in sys.modules if key
                        not in old_sys_modules]
    for new_module_name in new_module_names:
        assert not new_module_name.startswith(module_address)
    #                                                                         #
    ### Finished ensuring the module wasn't added to `sys.modules`. ###########
    


#def _check_module_tasting(module_path_or_address):
    #pass


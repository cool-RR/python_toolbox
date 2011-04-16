# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `` class.

See its documentation for more information.
'''

# blocktodo: Will need thread safety for when another thread is importing at
# the same time. probably make context manager for import lock from imp.

import imp
import sys
import os.path

from garlicsim.general_misc.third_party import mock as mock_module

from garlicsim.general_misc.temp_value_setters import TempImportHookSetter
from garlicsim.general_misc import import_tools


def mock_import(*args, **kwargs):
    return mock_module.Mock(name=repr(args, kwargs))

def taste_module(path_or_address):
    
    # blocktodo: implement address    
    path = path_or_address
    os.path.isfile(path)
    
    old_sys_modules = sys.modules[:] # blocktodo: Make context manager for this
    
    with TempImportHookSetter(mock_import):
        
        # Note that `import_by_path` is not affected by the import hook:
        tasted_module = import_tools.import_by_path(path)
        
    assert old_sys_modules == sys.modules
    
    return tasted_module
        
# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `taste_module` class.

See its documentation for more information.
'''

# blocktodo: Will need thread safety for when another thread is importing at
# the same time. probably make context manager for import lock from imp.

from __future__ import with_statement

import uuid
import sys
import os.path

from garlicsim.general_misc.temp_value_setters import TempImportHookSetter
from garlicsim.general_misc import address_tools
from garlicsim.general_misc import dict_tools
from garlicsim.general_misc import import_tools
from garlicsim.general_misc import context_managers

from .sys_modules_unchanged_assertor import SysModulesUnchangedAssertor
from .mock_importer import MockImporter

###############################################################################
#                                                                             #
# Importing stuff that would normally be auto-imported later. We're importing
# it now just so it will get into `sys.modules` so we could easily track
# changes to `sys.modules` when we do module-tasting.

import zlib
import encodings.utf_8 as _
try: # Available on Windows only:
    import encodings.mbcs as _
except ImportError:
    pass
#                                                                             #
###############################################################################


# blocktodo: test this is correct:
zip_import_uses_import_hook = (sys.version_info[:2] == (2, 5))

        
def taste_module(address):
    '''
    "Taste" a module, importing it without having it import other modules.
    
    Sometimes a module defines a few simple constants that you would like to
    check, like `__version__` for version number. You want to get the value of
    those, but you don't want to import the entire module because it might
    import other heavy modules, or it might be a huge package. The solution:
    Module-tasting.
    
    Example:
    
        >>> tasted_module = taste_module('my_module')
        >>> print(tasted_module.__version__)
        '0.9.2'
        
    Module-tasting imports the module while not letting it import any other
    module. Whenever the tasted module tries to import another module, it's
    being given a mock object instead. This also means that it's dangerous to
    taste modules that do non-trivial logic at import time.
    '''
    
    assert address_tools.is_address(address)
    path = import_tools.find_module(address)
    
    is_dotted_address = '.' in address    
    is_zip_module = '.zip' in path
        
    if not is_zip_module:
        assert os.path.exists(path)
        
    skip_first_import = is_zip_module and \
                        zip_import_uses_import_hook and \
                        not is_dotted_address
    
    with SysModulesUnchangedAssertor():
            
        name = 'tasted_module_%s' % uuid.uuid4() if not is_zip_module else None
        
        mock_importer = MockImporter(
            skip_first_import=skip_first_import
        )
        
        with TempImportHookSetter(mock_importer):
            
            tasted_module = import_tools.import_by_path(path,
                                                        name=name,
                                                        keep_in_sys_modules=False)
    
    return tasted_module
        
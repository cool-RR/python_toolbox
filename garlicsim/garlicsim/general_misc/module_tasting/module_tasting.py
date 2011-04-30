# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `` class.

See its documentation for more information.
'''

# blocktodo: Will need thread safety for when another thread is importing at
# the same time. probably make context manager for import lock from imp.

from __future__ import with_statement

import uuid
import __builtin__
import sys
import os.path

from garlicsim.general_misc.third_party import mock as mock_module

from garlicsim.general_misc.temp_value_setters import TempImportHookSetter
from garlicsim.general_misc import address_tools
from garlicsim.general_misc import dict_tools
from garlicsim.general_misc import import_tools
from garlicsim.general_misc import context_manager

from .sys_modules_unchanged_assertor import SysModulesUnchangedAssertor

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


class MockImporter(object):
    def __init__(self, skip_first_import=False):
        self.original_import = __builtin__.__import__
        self.skip_first_import = skip_first_import
        self.times_called = 0
        
    def __call__(self, name, *args, **kwargs):
        if self.skip_first_import and self.times_called == 0:
            self.times_called = 1
            return self.original_import(name, *args, **kwargs)
        else:
            self.times_called += 1
            return mock_module.Mock(name=name)

        
def taste_module(address):
    
    assert address_tools.is_address(address)
    path = import_tools.find_module(address)
    
    is_dotted_address = '.' in address    
    is_zip_module = '.zip' in path
        
    if not is_zip_module:
        assert os.path.exists(path)
        
    skip_first_import = is_zip_module and (zip_import_uses_import_hook and
                                           not is_dotted_address)
    
    with SysModulesUnchangedAssertor():
            
        name = 'tasted_module_%s' % uuid.uuid4() if not is_zip_module else None
        
        mock_importer = MockImporter(
            skip_first_import=skip_first_import
        )
        
        with TempImportHookSetter(mock_importer):
            
            # Note that `import_by_path` is not affected by the import hook, unless
            # it's a zip import:
            tasted_module = import_tools.import_by_path(path,
                                                        name=name,
                                                        keep_in_sys_modules=False)
    
    return tasted_module
        
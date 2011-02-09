# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing `import_tools.exists` on modules available through zip archives.'''

# todo: test package in zip, zip in zip, multiple root-level modules in zip.

import os

import pkg_resources
import nose.tools

from garlicsim.general_misc import sys_tools
from garlicsim.general_misc import cute_testing
from garlicsim.general_misc import import_tools
from garlicsim.general_misc.import_tools import exists

from . import resources as __resources_package
resources_package = __resources_package.__name__

def test_zip():
    '''Test `exists` works on zip-imported modules.'''
    
    assert not exists('zip_imported_module_bla_bla')
    
    zip_string = pkg_resources.resource_string(resources_package,
                                               'archive_with_module.zip')
    
    temp_dir = tempfile.mkdtemp(prefix='temp_test_garlicsim_')
    
    try:

        temp_zip_path = os.path.join(temp_dir, 'archive_with_module.zip')
        
        with open(temp_zip_path, 'wb') as temp_zip_file:
            
            temp_zip_file.write(zip_string)            
                
        assert not exists('zip_imported_module_bla_bla')
        
        with sys_tools.TempSysPathAdder(temp_zip_path):
            assert exists('zip_imported_module_bla_bla')
            
    finally:
        shutil.rmtree(temp_dir)
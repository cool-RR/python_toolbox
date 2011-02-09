# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing `import_tools.exists` on modules available through zip archives.'''

import pkg_resources
import nose.tools

from garlicsim.general_misc import temp_value_setters
from garlicsim.general_misc import cute_testing
from garlicsim.general_misc import import_tools
from garlicsim.general_misc.import_tools import exists

from . import resources as __resources_package
resources_package = __resources_package.__name__

def test_zip():
    '''Test `exists` works on zip-imported modules.'''
    
    zip_string = pkg_resources.resource_string(resources_package,
                                               'archive_with_module.zip')
    
    temp_dir = tempfile.mkdtemp(prefix='temp_test_garlicsim_')
    try:
    
        
    assert not exists('adfgadbnv5nrn')
    assert not exists('45gse_e5b6_DFDF')
    assert not exists('VWEV65hnrt___a4')
    assert exists('email')
    assert exists('re')
    assert exists('sys')
    nose.tools.assert_raises(Exception, lambda: exists('email.encoders'))
# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing `import_tools.exists` on modules available through zip archives.'''

# todotest: test package in zip, zip in zip, multiple root-level modules in
# zip.

import os
import tempfile
import shutil

from python_toolbox import sys_tools
from python_toolbox import cute_testing
from python_toolbox import import_tools
from python_toolbox import temp_file_tools
from python_toolbox.import_tools import exists


zip_string = (
    b'PK\x03\x04\x14\x00\x00\x00\x08\x00\xd0cI>c\xad\x8e3U\x00\x00\x00b\x00'
    b'\x00\x00\x1e\x00\x00\x00zip_imported_module_bla_bla.py\x1d\xcbA\x0e'
    b"@@\x0c\x05\xd0\xab\xfc]W\xe6\x02\xce\xe0\x0c\x1d\xa1h2\xa62-\x11\xa7'"
    b'\xf6\xef\x11\xd1`\xf3Y\x04\x8b5\x84xh]\x91u?\xac\x05\x87Y\xf1$\xb7zx\x86'
    b'U<ztc\x9b6\xbdd\xc6\xfeGOD\xd4ct\x97\x16\xa0\xf4\x11\x82V0/Z\x84\xf9'
    b'\x05PK\x01\x02\x17\x0b\x14\x00\x00\x00\x08\x00\xd0cI>c\xad\x8e3U\x00\x00'
    b'\x00b\x00\x00\x00\x1e\x00\x00\x00\x00\x00\x00\x00\x01\x00 \x00\x00\x00'
    b'\x00\x00\x00\x00zip_imported_module_bla_bla.pyPK\x05\x06\x00\x00\x00'
    b'\x00\x01\x00\x01\x00L\x00\x00\x00\x91\x00\x00\x00\x00\x00'
)


def test_zip():
    '''Test `exists` works on zip-imported modules.'''

    assert not exists('zip_imported_module_bla_bla')

    with temp_file_tools.create_temp_folder(
                                 prefix='test_python_toolbox_') as temp_folder:

        temp_zip_path = temp_folder / 'archive_with_module.zip'

        with temp_zip_path.open('wb') as temp_zip_file:
            temp_zip_file.write(zip_string)

        assert not exists('zip_imported_module_bla_bla')

        with sys_tools.TempSysPathAdder(temp_zip_path):
            assert exists('zip_imported_module_bla_bla')
            import zip_imported_module_bla_bla
            assert zip_imported_module_bla_bla.__doc__ == \
                   ('Module for testing `import_tools.exists` on zip-archived '
                    'modules.')



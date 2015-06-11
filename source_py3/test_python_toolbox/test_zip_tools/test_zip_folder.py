# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

try:
    import pathlib
except:
    from python_toolbox.third_party import pathlib


from python_toolbox import cute_testing
from python_toolbox import temp_file_tools

from python_toolbox import zip_tools


def test():
    with temp_file_tools.create_temp_folder() as temp_folder:
        assert isinstance(temp_folder, pathlib.Path)
        
        folder_to_zip = (temp_folder / 'folder_to_zip')
        folder_to_zip.mkdir()
        assert isinstance(folder_to_zip, pathlib.Path)
        
        (folder_to_zip / 'some_file.txt').open('w').write('hello there!')
        (folder_to_zip / 'some_other_file.txt').open('w').write(
                                                          'hello there again!')
        
        zip_file_path = temp_folder / 'archive.zip'
        assert isinstance(zip_file_path, pathlib.Path)
        zip_tools.zip_folder(folder_to_zip, temp_folder / 'archive.zip')
        
        assert zip_file_path.is_file()
        assert set(
            zip_tools.unzip_in_memory(zip_file_path.open('rb').read())
        ) == {
            ('folder_to_zip/some_file.txt', b'hello there!'), 
            ('folder_to_zip/some_other_file.txt', b'hello there again!'), 
        }
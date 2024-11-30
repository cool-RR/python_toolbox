# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import python_toolbox
from python_toolbox import temp_file_tools
from python_toolbox import cute_testing

from python_toolbox import file_tools


def test():
    with temp_file_tools.create_temp_folder(
                            prefix='test_python_toolbox_') as temp_folder:
        assert set(temp_folder.glob('*')) == set()
        file_1 = temp_folder / 'file_1.txt'
        assert not file_1.exists()
        file_tools.atomic_create_and_write(file_1, "Meow meow I'm a cat.")
        assert set(temp_folder.glob('*')) == {file_1}
        with file_1.open('r') as file:
            assert file.read() == "Meow meow I'm a cat."

        #######################################################################

        file_2 = temp_folder / 'file_2.txt'
        with file_tools.atomic_create(file_2) as file:
            file.write('Hurr durr')
            assert not file_2.exists()
            assert len(set(temp_folder.glob('*'))) == 2

        assert file_2.exists()
        assert len(set(temp_folder.glob('*'))) == 2
        assert set(temp_folder.glob('*')) == {file_1, file_2}
        with file_2.open('r') as file:
            assert file.read() == 'Hurr durr'

        #######################################################################


        file_3 = temp_folder / 'file_3.txt'

        with cute_testing.RaiseAssertor(ZeroDivisionError):
            with file_tools.atomic_create(file_3) as file:
                file.write('bloop bloop bloop')
                assert not file_3.exists()
                assert len(set(temp_folder.glob('*'))) == 3
                1 / 0

        assert not file_3.exists()
        assert len(set(temp_folder.glob('*'))) == 2
        assert set(temp_folder.glob('*')) == {file_1, file_2}


        #######################################################################

        file_4 = temp_folder / 'file_4.txt'
        test_text = "Hello 世界" # Mix of ASCII and Unicode characters
        
        # Test writing with explicit UTF-8 encoding
        file_tools.atomic_create_and_write(file_4, test_text, encoding='utf-8')
        with file_4.open('r', encoding='utf-8') as file:
            assert file.read() == test_text

        # Test writing with different encoding (e.g. latin-1)
        file_5 = temp_folder / 'file_5.txt'
        latin_text = "Café" # Contains non-ASCII character
        file_tools.atomic_create_and_write(file_5, latin_text, encoding='latin-1')
        with file_5.open('r', encoding='latin-1') as file:
            assert file.read() == latin_text

        # Test atomic_create with encoding
        file_6 = temp_folder / 'file_6.txt'
        with file_tools.atomic_create(file_6, encoding='utf-8') as file:
            file.write(test_text)
        with file_6.open('r', encoding='utf-8') as file:
            assert file.read() == test_text

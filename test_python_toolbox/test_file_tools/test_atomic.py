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

# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `temp_file_tools.create_temp_folder`.'''

import tempfile
import os.path
import pathlib

import python_toolbox

from python_toolbox.temp_file_tools import create_temp_folder

class MyException(Exception):
    pass


def test_basic():
    with create_temp_folder() as tf1:
        assert isinstance(tf1, pathlib.Path)
        assert tf1.exists()
        assert tf1.is_dir()

        tf2 = create_temp_folder()
        with tf2 as tf2:
            assert isinstance(tf2, pathlib.Path)
            assert tf2.exists()
            assert tf2.is_dir()

        assert not tf2.exists()
        assert not tf2.is_dir()

        assert tf1.exists()
        assert tf1.is_dir()
        file_path = (tf1 / 'my_file')
        with file_path.open('w') as my_file:
            my_file.write('Woo hoo!')

        assert file_path.exists()
        assert file_path.is_file()

        with file_path.open('r') as my_file:
            assert my_file.read() == 'Woo hoo!'

    assert not tf1.exists()
    assert not tf1.is_dir()

    assert not file_path.exists()
    assert not file_path.is_file()

def test_exception():
    try:
        with create_temp_folder() as tf1:
            assert isinstance(tf1, pathlib.Path)
            assert tf1.exists()
            assert tf1.is_dir()
            file_path = (tf1 / 'my_file')
            with file_path.open('w') as my_file:
                my_file.write('Woo hoo!')

            assert file_path.exists()
            assert file_path.is_file()
            raise MyException
    except MyException:
        assert not tf1.exists()
        assert not tf1.is_dir()
        assert not file_path.exists()
        assert not file_path.is_file()

def test_without_pathlib():
    with create_temp_folder() as tf1:
        assert os.path.exists(str(tf1))
        assert os.path.isdir(str(tf1))

        tf2 = create_temp_folder()
        with tf2 as tf2:
            assert os.path.exists(str(tf2))
            assert os.path.isdir(str(tf2))

        assert not os.path.exists(str(tf2))
        assert not os.path.isdir(str(tf2))

        assert os.path.exists(str(tf1))
        assert os.path.isdir(str(tf1))

        file_path = os.path.join(str(tf1), 'my_file')
        with open(file_path, 'w') as my_file:
            my_file.write('Woo hoo!')

        assert os.path.exists(file_path)
        assert os.path.isfile(file_path)

        with open(file_path, 'r') as my_file:
            assert my_file.read() == 'Woo hoo!'

    assert not os.path.exists(str(tf1))
    assert not os.path.isdir(str(tf1))

    assert not os.path.exists(file_path)
    assert not os.path.isdir(file_path)


def test_prefix_suffix():
    with create_temp_folder(prefix='hocus', suffix='pocus') as tf1:
        assert tf1.name.startswith('hocus')
        assert tf1.name.endswith('pocus')

def test_parent_folder():
    with create_temp_folder() as tf1:
        with create_temp_folder(parent_folder=str(tf1)) as tf2:
            assert isinstance(tf2, pathlib.Path)
            assert str(tf2).startswith(str(tf1))

def test_chmod():
    with create_temp_folder(chmod=0o777) as liberal_temp_folder, \
                   create_temp_folder(chmod=0o000) as conservative_temp_folder:
        # Doing a very weak test of chmod because not everything is supported
        # on Windows.
        assert (liberal_temp_folder.stat().st_mode & 0o777) > \
                              (conservative_temp_folder.stat().st_mode & 0o777)

        # Making `conservative_temp_folder` writeable again so it could be
        # deleted in cleanup:
        conservative_temp_folder.chmod(0o777)


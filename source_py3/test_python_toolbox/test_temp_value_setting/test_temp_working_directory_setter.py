# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing `python_toolbox.temp_value_setting.TempWorkingDirectorySetter`.'''

import os
try:
    import pathlib
except:
    from python_toolbox.third_party import pathlib

import shutil
import tempfile

from python_toolbox import cute_testing
from python_toolbox import temp_file_tools

from python_toolbox.temp_value_setting import \
     TempWorkingDirectorySetter

class MyException(Exception):
    pass

def test():
    '''Test basic workings of `TempWorkingDirectorySetter`.'''
    with temp_file_tools.create_temp_folder(
                                 prefix='test_python_toolbox_') as temp_folder:
        old_cwd = os.getcwd()
        with TempWorkingDirectorySetter(temp_folder):
            
            # Note that on Mac OS, the working dir will be phrased differently,
            # so we can't do `assert os.getcwd() == temp_dir`. Instead we'll
            # create a small file and check we can access it:
            
            with pathlib.Path('just_a_file').open('w') as my_file:
                my_file.write(u'One two three.')
            
            with pathlib.Path('just_a_file').open('r') as my_file:
                assert my_file.read() == 'One two three.'
        
        with (temp_folder / 'just_a_file').open('r') as my_file:
            assert my_file.read() == 'One two three.'
        
        assert os.getcwd() == old_cwd
    
    
def test_exception():
    '''Test `TempWorkingDirectorySetter` recovering from exception in suite.'''
    # Not using `assert_raises` here because getting the `with` suite in there
    # would be tricky.
    with temp_file_tools.create_temp_folder(
                                 prefix='test_python_toolbox_') as temp_folder:
        old_cwd = os.getcwd()
        try:
            with TempWorkingDirectorySetter(temp_folder):
                
                # Note that on Mac OS, the working dir will be phrased
                # differently, so we can't do `assert os.getcwd() ==
                # temp_folder`. Instead we'll create a small file and check we
                # can access it:
                
                with pathlib.Path('just_a_file').open('w') as my_file:
                    my_file.write(u'One two three.')
                
                with pathlib.Path('just_a_file').open('r') as my_file:
                    assert my_file.read() == 'One two three.'
                
                raise MyException
            
        except MyException:

            with (temp_folder / 'just_a_file').open('r') as my_file:
                assert my_file.read() == 'One two three.'
                
        else:
            raise Exception
        
        with (temp_folder / 'just_a_file').open('r') as my_file:
            assert my_file.read() == 'One two three.'

        
def test_as_decorator():
    '''Test `TempWorkingDirectorySetter` used as a decorator.'''
    with temp_file_tools.create_temp_folder(
                                 prefix='test_python_toolbox_') as temp_folder:
        old_cwd = os.getcwd()
        @TempWorkingDirectorySetter(temp_folder)
        def f():
            # Note that on Mac OS, the working dir will be phrased differently,
            # so we can't do `assert os.getcwd() == temp_folder`. Instead we'll
            # create a small file and check we can access it:
            
            with pathlib.Path('just_a_file').open('w') as my_file:
                my_file.write(u'One two three.')
            
            with pathlib.Path('just_a_file').open('r') as my_file:
                assert my_file.read() == 'One two three.'
                
        f()
        
        cute_testing.assert_polite_wrapper(f)
        
        with (temp_folder / 'just_a_file').open('r') as my_file:
            assert my_file.read() == 'One two three.'
        
        assert os.getcwd() == old_cwd
        
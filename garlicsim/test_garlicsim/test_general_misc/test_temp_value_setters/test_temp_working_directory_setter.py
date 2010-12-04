import os
import shutil
import tempfile

from garlicsim.general_misc.temp_value_setters import TempWorkingDirectorySetter

class MyException(Exception):
    pass

def test():
    temp_dir = tempfile.mkdtemp(prefix='temp_garlicsim_')
    try:
        old_cwd = os.getcwd()
        with TempWorkingDirectorySetter(temp_dir):
            assert os.getcwd() == temp_dir
        assert os.getcwd() == old_cwd        
    finally:
        shutil.rmtree(temp_dir)
    
    
def test_exception():
    # Not using `assert_raises` here because getting the `with` suite in there
    # will be tricky.
    temp_dir = tempfile.mkdtemp(prefix='temp_garlicsim_')
    try:
        old_cwd = os.getcwd()
        try:
            with TempWorkingDirectorySetter(temp_dir):
                assert os.getcwd() == temp_dir
                raise MyException
        except MyException:
            assert os.getcwd() == old_cwd
        else:
            raise Exception
        assert os.getcwd() == old_cwd
        
    finally:
        shutil.rmtree(temp_dir)
    
    
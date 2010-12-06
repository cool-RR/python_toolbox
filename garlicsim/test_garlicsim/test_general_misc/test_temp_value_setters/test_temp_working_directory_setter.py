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
            
            # Note that on Mac OS, the working dir will be phrased differently,
            # so we can't do `assert os.getcwd() == temp_dir`. Instead we'll
            # create a small file and check we can access it:
            
            with open('just_a_file', 'w') as my_file:
                my_file.write("One two three.")
            
            with open('just_a_file', 'r') as my_file:
                assert my_file.read() == "One two three."
        
        with open(os.path.join(temp_dir, 'just_a_file'), 'r') as my_file:
            assert my_file.read() == "One two three."
        
        assert os.getcwd() == old_cwd
    finally:
        shutil.rmtree(temp_dir)
    
    
def test_exception():
    # Not using `assert_raises` here because getting the `with` suite in there
    # would be tricky.
    temp_dir = tempfile.mkdtemp(prefix='temp_garlicsim_')
    try:
        old_cwd = os.getcwd()
        try:
            with TempWorkingDirectorySetter(temp_dir):
                
                # Note that on Mac OS, the working dir will be phrased
                # differently, so we can't do `assert os.getcwd() == temp_dir`.
                # Instead we'll create a small file and check we can access it:
                
                with open('just_a_file', 'w') as my_file:
                    my_file.write("One two three.")
                
                with open('just_a_file', 'r') as my_file:
                    assert my_file.read() == "One two three."
                
                raise MyException
            
        except MyException:

            with open(os.path.join(temp_dir, 'just_a_file'), 'r') as my_file:
                assert my_file.read() == "One two three."
                
        else:
            raise Exception
        
        with open(os.path.join(temp_dir, 'just_a_file'), 'r') as my_file:
            assert my_file.read() == "One two three."
        
    finally:
        shutil.rmtree(temp_dir)
    
    
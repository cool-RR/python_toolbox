import os.path
import shutil
import tempfile

from garlicsim.general_misc.temp_value_setters import \
    TempWorkingDirectorySetter
from garlicsim.general_misc import sys_tools
from garlicsim.general_misc import import_tools

import garlicsim.scripts.start_simpack
start_simpack_file = garlicsim.scripts.start_simpack.__file__




def test():
    # tododoc: do this. Don't forget to test the simpack works.
    
    # Asserting we don't have a `my_simpack` on path already in some other
    # place:
    assert not import_tools.exists('my_simpack')
    
    temp_dir = tempfile.mkdtemp(prefix='temp_garlicsim_')
    try:
        with TempWorkingDirectorySetter(temp_dir):
            with sys_tools.OutputCapturer() as output_capturer:
                garlicsim.scripts.start_simpack.execute(
                    argv=['start_simpack.py', 'my_simpack']
                )
            assert output_capturer.output == \
                ("`my_simpack` simpack created successfully! Explore the "
                 "`my_simpack` folder and start filling in the contents of "
                 "your new simpack.\n")
            simpack_path = os.path.join(temp_dir, 'my_simpack')
            assert os.path.isdir(simpack_path)
            with sys_tools.TempSysPathAdder(temp_dir):
                import my_simpack
            
            
            
            
    finally:
        shutil.rmtree(temp_dir)

        
def test_implicit_help():
    pass#tododoc
        

def test_explicit_help():
    pass#tododoc
    
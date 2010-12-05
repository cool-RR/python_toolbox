import os
import shutil
import tempfile

from garlicsim.general_misc.temp_value_setters import \
    TempWorkingDirectorySetter

import garlicsim.scripts.start_simpack




def test():
    # tododoc: do this
    temp_dir = tempfile.mkdtemp(prefix='temp_garlicsim_')
    try:
        with TempWorkingDirectorySetter(temp_dir):
            os.system
            
    finally:
        shutil.rmtree(temp_dir)
import os
import shutil
import tempfile




def test():
    # tododoc: do this or not? want harddrive
    temp_dir = tempfile.mkdtemp(prefix='temp_garlicsim_')
    try:
        assert 1 + 1 == 2
    finally:
        shutil.rmtree(temp_dir)
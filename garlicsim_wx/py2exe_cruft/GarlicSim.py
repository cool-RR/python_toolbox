# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''A script for starting GarlicSim from an executable.'''

import sys
import os.path
import multiprocessing

if False:
    # The `if False` is important here, even though `almost_import_stdlib`
    # already has one wrapping it inside, because `almost_import_stdlib.py`
    # won't get packaged at all with py2exe, so trying to import it will raise
    # an ImportError.
    import almost_import_stdlib

use_psyco = False
try:
    import psyco
    use_psyco = True
except ImportError:
    pass
    
    
if __name__ == '__main__':
    multiprocessing.freeze_support()
    
    import garlicsim
    import garlicsim_wx
    
    if use_psyco:
        psyco.full()
    garlicsim_wx.start()
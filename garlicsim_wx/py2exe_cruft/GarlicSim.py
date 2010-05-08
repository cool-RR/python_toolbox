# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''tododoc'''

import sys
import os.path
import multiprocessing

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
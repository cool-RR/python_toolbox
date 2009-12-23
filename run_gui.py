#!/usr/bin/env python

# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
A little module to start the garlicsim_wx GUI without installing it.
'''

import sys
import os.path



path_to_garlicsim = os.path.abspath('garlicsim')
path_to_garlicsim_wx = os.path.abspath('garlicsim_wx')

sys.path += [path_to_garlicsim, path_to_garlicsim_wx]



arguments = sys.argv[1:]
debug = '-debug' in arguments



use_psyco = False
if not debug:
    try:
        import psyco
        use_psyco = True
    except ImportError:
        pass
    
    
    
if __name__ == '__main__':
    
    if use_psyco:
        psyco.full()
        
    import garlicsim
    import garlicsim_wx
        
    garlicsim_wx.start()
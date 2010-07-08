#!/usr/bin/env python

# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''A little module to start the garlicsim_wx GUI without installing it.'''

import sys
import os.path


path_to_garlicsim = os.path.abspath('garlicsim')
path_to_garlicsim_lib = os.path.abspath('garlicsim_lib')
path_to_garlicsim_wx = os.path.abspath('garlicsim_wx')

for path in [path_to_garlicsim, path_to_garlicsim_lib, path_to_garlicsim_wx]:
    if path not in sys.path:
        sys.path.append(path)

arguments = sys.argv[1:]
debug = '-debug' in arguments

use_psyco = False
if not debug:
    try:
        import psyco
        use_psyco = True
    except ImportError:
        pass
    
    
def start():
    
    import garlicsim
    import garlicsim_wx
    
    if use_psyco:
        psyco.full()
    garlicsim_wx.start()
        
    #import cProfile
    #cProfile.run('garlicsim_wx.start()', sort=2)

if __name__ == '__main__':
    start()
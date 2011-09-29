#!/usr/bin/env python

# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''A little module to start the `garlicsim_wx` GUI without installing it.'''

import sys
import os.path


path_to_garlicsim = os.path.realpath('garlicsim')
path_to_garlicsim_lib = os.path.realpath('garlicsim_lib')
path_to_garlicsim_wx = os.path.realpath('garlicsim_wx')

for path in [path_to_garlicsim, path_to_garlicsim_lib, path_to_garlicsim_wx]:
    if path not in sys.path:
        sys.path.append(path)

arguments = sys.argv[1:]

use_psyco = False
if not ('--psyco=off' in arguments):
    try:
        import psyco
        use_psyco = True
    except ImportError:
        pass
    
    
def start():
    '''Start the GUI.'''
    
    import garlicsim
    import garlicsim_wx
    
    if use_psyco:
        psyco.full()
    garlicsim_wx.start()
    

if __name__ == '__main__':
    start()

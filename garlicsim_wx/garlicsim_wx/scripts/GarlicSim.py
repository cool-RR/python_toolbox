#!/usr/bin/env python

# Copyright 2009-2011 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''Script that starts the `garlicsim_wx` GUI.'''

import sys 
import os.path


use_psyco = False
if not ('--psyco=off' in sys.argv):
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
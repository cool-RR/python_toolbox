# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
tododoc
'''

from particles import *

import garlicsim

class Meta(object):
    force_cruncher = garlicsim.asynchronous_crunching.\
                     crunchers_warehouse.crunchers['CruncherThread']
    # We're forcing CruncherThread because of ETS + multiprocessing bug

wx_installed = False
try:
    import wx
    wx_installed = True
except ImportError:
    pass

if wx_installed:
    from particles_wx import *
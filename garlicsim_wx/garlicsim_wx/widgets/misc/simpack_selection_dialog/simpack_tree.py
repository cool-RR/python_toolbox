# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `SimpackTree` class.

See its documentation for more info.
'''

import os
import sys
import glob
import pkgutil

import wx
import pkg_resources

from garlicsim.general_misc.cmp_tools import underscore_hating_cmp
from garlicsim.general_misc import address_tools
from garlicsim.general_misc import path_tools
from garlicsim.general_misc import import_tools
from garlicsim.general_misc import package_finder
from garlicsim_wx.general_misc import wx_tools

import garlicsim_wx

from . import images as __images_package
images_package = __images_package.__name__


class SimpackTree(wx.Panel):
    
    def __init__(self, simpack_selection_dialog):
        wx.Panel.__init__(
            self,
            simpack_selection_dialog,
        )
        
        assert isinstance(simpack_selection_dialog, SimpackSelectionDialog)
        self.simpack_selection_dialog = simpack_selection_dialog
        
        self.SetBackgroundColour(wx.NamedColor('Black'))

        
from .simpack_selection_dialog import SimpackSelectionDialog
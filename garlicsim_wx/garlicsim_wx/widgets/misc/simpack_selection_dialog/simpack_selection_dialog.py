# Copyright 2009-2011 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
This module defines the `SimpackSelectionDialog` class.

See its documentation for more info.
'''

import os
import glob
import pkgutil

import wx

from garlicsim.general_misc.cmp_tools import underscore_hating_cmp
from garlicsim.general_misc import import_tools
from garlicsim_wx.widgets.general_misc.cute_dialog import CuteDialog


class SimpackSelectionDialog(CuteDialog, wx.SingleChoiceDialog):
    '''Dialog for selecting a simpack when creating a new gui project.'''
    
    def __init__(self, parent):
        self.make_simpack_list()
        wx.SingleChoiceDialog.__init__(
            self,
            parent,
            'Choose a simulation package for your new simulation:',
            'Choose simulation package',
            self.list_of_simpacks,
            wx.CHOICEDLG_STYLE
        )
        CuteDialog.__init__(self, parent, skip_dialog_init=True)
        
        
    def make_simpack_list(self):
        '''Make a list of available simpacks.'''
        import garlicsim_lib.simpacks as simpacks
        self.list_of_simpacks = [
            module_name for (importer, module_name, is_package)
            in pkgutil.iter_modules(simpacks.__path__)
        ]
        self.list_of_simpacks.sort(cmp=underscore_hating_cmp)
        

    def get_simpack_selection(self):
        '''Import the selected simpack and return it.'''
        string = self.GetStringSelection()
        result = import_tools.normal_import('garlicsim_lib.simpacks.' + string)
        return result




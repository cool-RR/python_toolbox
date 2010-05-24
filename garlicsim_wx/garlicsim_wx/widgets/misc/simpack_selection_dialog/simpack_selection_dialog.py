# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
This module defines the SimpackSelectionDialog class.

See its documentation for more info.
'''

import os
import glob
import pkgutil

import wx

from simpack_name_cmp import simpack_name_cmp


class SimpackSelectionDialog(wx.SingleChoiceDialog):
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
        
    def make_simpack_list(self):
        '''Make a list of available simpacks.'''
        import garlicsim_lib.simpacks as simpacks
        self.list_of_simpacks = [
            module_name for (importer, module_name, is_package)
            in pkgutil.iter_modules(simpacks.__path__)
        ]
        self.list_of_simpacks.sort(cmp=simpack_name_cmp)
        

    def get_simpack_selection(self):
        '''Import the selected simpack and return it.'''
        string = self.GetStringSelection()
        result = __import__('garlicsim_lib.simpacks.' + string,
                            fromlist=[''])
        return result




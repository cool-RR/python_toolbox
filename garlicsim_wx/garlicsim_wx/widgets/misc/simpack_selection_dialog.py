# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
This module defines the SimpackSelectionDialog class.

See its documentation for more info.
'''

import os
import glob
import wx

class SimpackSelectionDialog(wx.SingleChoiceDialog):
    '''Dialog for selecting a simpack when creating a new gui project.'''
    
    def __init__(self, parent):
        self.make_simpack_list()
        wx.SingleChoiceDialog.__init__(self, parent,
                                       "Choose simulation package",
                                       "Choose simulation package",
                                       self.list_of_simpacks,
                                       wx.CHOICEDLG_STYLE)
        
    def make_simpack_list(self):
        '''Make a list of available simpacks.'''
        import garlicsim_lib.simpacks as simpacks
        self.list_of_simpacks = find_subpackages(simpacks)

    def get_simpack_selection(self):
        '''Import the selected simpack and return it.'''
        string = self.GetStringSelection()
        result = __import__("garlicsim_lib.simpacks." + string,
                            fromlist=[''])
        return result


def find_subpackages(module):
    '''
    Find all subpackages of a module.
    # todo: module? really?
    '''
    result = []
    for thing in os.listdir(os.path.dirname(module.__file__)):
        full = os.path.join(os.path.dirname(module.__file__), thing)
        if os.path.isdir(full):
            if glob.glob(os.path.join(full, '__init__.py*')):
                result.append(thing)
    return result




# Copyright 2009 Ram Rachum.
# This program is not licensed for distribution and may not be distributed.

import os, glob
import wx

class SimpackSelectionDialog(wx.SingleChoiceDialog):
    def __init__(self,parent,id):
        self.make_simpack_list()
        wx.SingleChoiceDialog.__init__(self,parent,
                                        "Choose simulation package","Choose simulation package",
                                        self.list_of_simpacks,wx.CHOICEDLG_STYLE)

    def make_simpack_list(self):
        import simulation_packages
        self.list_of_simpacks=find_subpackages(simulation_packages)

    def get_simpack_selection(self):
        string=self.GetStringSelection()
        result=__import__("simulation_packages."+string,fromlist=[''])
        return result


def find_subpackages(module):
    result=[]
    for thing in os.listdir(os.path.dirname(module.__file__)):
        full=os.path.join(os.path.dirname(module.__file__),thing)
        if os.path.isdir(full):
            if glob.glob(os.path.join(full, '__init__.py*'))!=[]:
                result.append(thing)
    return result




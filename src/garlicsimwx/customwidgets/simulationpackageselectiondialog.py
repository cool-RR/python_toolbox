import os, glob
import wx

class SimulationPackageSelectionDialog(wx.SingleChoiceDialog):
    def __init__(self,parent,id):
        self.make_simulation_packages_list()
        wx.SingleChoiceDialog.__init__(self,parent,
                                        "Choose simulation package","Choose simulation package",
                                        self.list_of_simulation_packages,wx.CHOICEDLG_STYLE)

    def make_simulation_packages_list(self):
        import simulations
        self.list_of_simulation_packages=find_subpackages(simulations)

    def get_simulation_package_selection(self):
        string=self.GetStringSelection()
        result=__import__("simulations."+string,fromlist=[''])
        return result


def find_subpackages(module):
    result=[]
    for thing in os.listdir(os.path.dirname(module.__file__)):
        full=os.path.join(os.path.dirname(module.__file__),thing)
        if os.path.isdir(full):
            if glob.glob(os.path.join(full, '__init__.py*'))!=[]:
                result.append(thing)
    return result




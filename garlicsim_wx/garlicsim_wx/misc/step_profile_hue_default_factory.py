import garlicsim_wx
from garlicsim_wx.general_misc import misc_tools
from garlicsim.general_misc import dict_tools

class StepProfileHueDefaultFactory(object):
    def __init__(self, gui_project):
        self.gui_project = gui_project
        assert isinstance(self.gui_project, garlicsim_wx.GuiProject)
        
    def __call__(self):
        hues = dict_tools.get_contained(
            self.gui_project.step_profiles_to_hues,
            self.gui_project.step_profiles
        )
        return misc_tools.find_clear_place_on_circle(hues, circle_size=1)
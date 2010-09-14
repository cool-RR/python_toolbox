import garlicsim_wx

class StepProfileHueDefaultFactory(object):
    def __init__(self, gui_project):
        self.gui_project = gui_project
        assert isinstance(self.gui_project, garlicsim_wx.GuiProject)
        
    def __call__(self):
        
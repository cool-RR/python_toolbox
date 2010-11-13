
import wx

from garlicsim.general_misc import string_tools

import garlicsim


class CruncherTextScrolledPanel(wx.lib.scrolledpanel.ScrolledPanel):
    def __init__(self, cruncher_selection_dialog):
        self.cruncher_selection_dialog = cruncher_selection_dialog
        wx.lib.scrolledpanel.ScrolledPanel.__init__(self, cruncher_selection_dialog)
        self.SetupScrolling()
        self.SetMinSize((self.MinSize[0], 300))
        
        self.main_v_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.cruncher_text = wx.StaticText(
            self,
            label=''
        )
        self.main_v_sizer.Add(self.cruncher_text, 1, wx.EXPAND)
        
        self.cruncher_unavailability_text = wx.StaticText(
            self,
            label=''
        )
        self.cruncher_unavailability_text.SetForegroundColour(
            wx.Colour(100, 0, 0)
        )
        self.main_v_sizer.Add(self.cruncher_unavailability_text, 1, wx.EXPAND)
        
        #self.general_text.SetSize((self.ClientSize[0] - 20, -1))
        #self.cruncher_text.Wrap(
            #self.ClientSize[0]# - self.cruncher_list_box.BestSize[0] - 20
        #)
        #self.cruncher_text.SetSize(self.cruncher_text.GetEffectiveMinSize())
        self.SetSizer(self.main_v_sizer)
        
    def update(self):
        cruncher_type = self.cruncher_selection_dialog.selected_cruncher_type
        self.cruncher_text.SetLabel(cruncher_type.gui_explanation)
        availability = \
            self.cruncher_selection_dialog.cruncher_types_availability
        if availability == False:
            self.cruncher_unavailability_text.SetLabel(
                getattr(availability, 'reason', '')
            )
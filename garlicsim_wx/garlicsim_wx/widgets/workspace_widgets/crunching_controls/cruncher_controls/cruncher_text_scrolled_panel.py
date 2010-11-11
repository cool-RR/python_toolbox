
import wx

from garlicsim.general_misc import string_tools

import garlicsim


class CruncherTextScrolledPanel(wx.lib.scrolledpanel.ScrolledPanel):
    def __init__(self, cruncher_selection_dialog):
        wx.lib.scrolledpanel.ScrolledPanel.__init__(self, cruncher_selection_dialog)
        self.SetupScrolling()
        self.cruncher_text = wx.StaticText(
            self,
            label=string_tools.docstring_trim(
                garlicsim.asynchronous_crunching.crunchers.ThreadCruncher.\
                __doc__
            )
        )
        #self.general_text.SetSize((self.ClientSize[0] - 20, -1))
        self.cruncher_text.Wrap(
            self.ClientSize[0]# - self.cruncher_list_box.BestSize[0] - 20
        )
        #self.cruncher_text.SetSize(self.cruncher_text.GetEffectiveMinSize())
        
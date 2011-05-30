# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `CruncherTextScrolledPanel` class.

See its documentation for more details.
'''

from __future__ import with_statement

import wx

from garlicsim.general_misc import string_tools
from garlicsim_wx.general_misc import wx_tools
from garlicsim_wx.widgets.general_misc.cute_window import CuteWindow

import garlicsim


class CruncherTextScrolledPanel(wx.lib.scrolledpanel.ScrolledPanel,
                                CuteWindow):
    '''Widget for showing information about the selected cruncher type.'''
    
    def __init__(self, cruncher_selection_dialog):
        self.cruncher_selection_dialog = cruncher_selection_dialog
        wx.lib.scrolledpanel.ScrolledPanel.__init__(self,
                                                    cruncher_selection_dialog)
        self.set_good_background_color()
        self.SetMinSize((530, 300))
        self.SetHelpText('Explanation about the currently selected cruncher '
                         'type.')
        
        self.main_v_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.cruncher_text = wx.StaticText(
            self,
            label=''
        )
        self.cruncher_text.Wrap(self._get_wrap_width())
        self.main_v_sizer.Add(self.cruncher_text, 0, wx.EXPAND)
        
        self.main_v_sizer.AddSpacer((1, 20))
        
        self.cruncher_unavailability_text = wx.StaticText(
            self,
            label=''
        )
        self.cruncher_unavailability_text.Wrap(self._get_wrap_width())
        self.cruncher_unavailability_text.SetForegroundColour(
            wx.Colour(170, 0, 0)
        )
        self.main_v_sizer.Add(self.cruncher_unavailability_text, 0, wx.EXPAND)
        
        #self.general_text.SetSize((self.ClientSize[0] - 20, -1))
        #self.cruncher_text.Wrap(
            #self.ClientSize[0]# - self.cruncher_list_box.BestSize[0] - 20
        #)
        #self.cruncher_text.SetSize(self.cruncher_text.GetEffectiveMinSize())
        self.SetSizer(self.main_v_sizer)
        self.SetupScrolling()
        
        
    def _get_wrap_width(self):
        return (self.GetClientSize()[0] - 10)

    
    def update(self):
        '''Update to show information about the current cruncher type.'''
        with self.freezer:
            cruncher_type = \
                self.cruncher_selection_dialog.selected_cruncher_type
            self.cruncher_text.SetLabel(cruncher_type.gui_explanation)
            self.cruncher_text.Wrap(self._get_wrap_width())
            availability = \
                self.cruncher_selection_dialog.cruncher_types_availability[
                    cruncher_type
                ]
            unavailibility_text = getattr(availability, 'reason', '') if \
                                  (availability == False) else ''
            self.cruncher_unavailability_text.SetLabel(unavailibility_text)
            self.cruncher_unavailability_text.Wrap(self._get_wrap_width())
            self.main_v_sizer.Layout()
            self.SetupScrolling()
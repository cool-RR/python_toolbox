# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `StateReprViewer` class.

See its documentation for more info.
'''

import wx
from garlicsim_wx.widgets import WorkspaceWidget
import garlicsim.general_misc.dict_tools as dict_tools
from garlicsim_wx.general_misc.flag_raiser import FlagRaiser
from garlicsim_wx.general_misc import wx_tools
from garlicsim_wx.widgets.general_misc.cute_panel import CutePanel


__all__ = ['StateReprViewer']


class StateReprViewer(CutePanel, WorkspaceWidget):
    '''Widget for showing the repr of the active state.'''
    def __init__(self, frame):
        CutePanel.__init__(self, frame, size=(300, 300),
                           style=wx.SUNKEN_BORDER)
        WorkspaceWidget.__init__(self, frame)

        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        
        self.text_ctrl = wx.TextCtrl(
            self,
            style=wx.TE_MULTILINE | wx.NO_BORDER
        )
        
        font_size = 12 if wx_tools.is_mac else 9
        
        font = wx.Font(font_size, wx.DEFAULT, wx.NORMAL, wx.BOLD, False,
                       u'Courier New')
        self.text_ctrl.SetFont(font)
        
        self.sizer_v = wx.BoxSizer(wx.VERTICAL)
        self.sizer_h = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_v.Add(self.sizer_h, 1, wx.EXPAND)
        self.sizer_h.Add(self.text_ctrl, 1, wx.EXPAND)
        
        self.SetSizer(self.sizer_v)
        self.sizer_v.Layout()
        
        self.state = None
        
        self.needs_recalculation_flag = True
        
        self.needs_update_emitter = \
            self.gui_project.emitter_system.make_emitter(
                inputs=(
                    self.gui_project.active_node_changed_or_modified_emitter,
                    # todo: put the active_state_changed whatever here
                    ),
                outputs=(
                    FlagRaiser(self, 'needs_recalculation_flag',
                               function=self._recalculate, delay=0.03),
                    ),
                name='state_repr_viewer_needs_recalculation',
            )
        
        self.bind_event_handlers(StateReprViewer)
    

    def _recalculate(self):
        '''Recalculate the widget.'''
        if self.needs_recalculation_flag:
            if self.gui_project:
                active_state = self.gui_project.get_active_state()        
                if active_state:
                    if active_state is not self.state:
                        self.state = active_state
                        state_repr = dict_tools.fancy_string(
                            vars(active_state)
                        )
                        self.text_ctrl.SetValue(state_repr)
            self.needs_recalculation_flag = False
        
            
    def _on_paint(self, event):
        '''EVT_PAINT handler.'''
        event.Skip()
        # Notice that we are not checking the `needs_recalculation_flag` here.
        # The FlagRaiser's 30ms delay is small enough, and we don't need to
        # have very fast response time in the state repr viewer, so we can
        # afford to wait another 30ms before an update.
        
         
        
    

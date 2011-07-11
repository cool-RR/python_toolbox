# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `StateViewer` class.

See its documentation for more information.
'''

import itertools

import wx

from garlicsim_wx.widgets.general_misc.cute_scrolled_panel import \
                                                              CuteScrolledPanel

import garlicsim
import garlicsim_wx
from garlicsim.general_misc.infinity import infinity
from garlicsim_wx.general_misc import wx_tools


class StateViewer(CuteScrolledPanel, garlicsim_wx.widgets.WorkspaceWidget):
    '''Widget for showing a state of the `queue` simpack.'''
    def __init__(self, frame):
        CuteScrolledPanel.__init__(self, frame, style=wx.SUNKEN_BORDER)
        garlicsim_wx.widgets.WorkspaceWidget.__init__(self, frame)
        
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        
        self.SetupScrolling()
        
        self.bind_event_handlers(StateViewer)
        
        self.state = None
        '''The current state being displayed.'''
        
        self.font = wx.Font(12, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL,
                            wx.FONTWEIGHT_BOLD, face='Courier New')        
        
        self.gui_project.active_node_changed_or_modified_emitter.add_output(
            lambda: self.load_state(self.gui_project.get_active_state())
        )

        
    def load_state(self, state):
        '''Set the state to be displayed.'''
        if state is None:
            return
        self.state = state
        self.Refresh()

        
    def _on_paint(self, event):
        
        event.Skip()
        
        state = self.state
        dc = wx.BufferedPaintDC(self)
        
        dc.SetBackground(wx_tools.colors.get_background_brush())
        dc.Clear()
        
        if state is None:
            return
        
        dc.SetBackgroundMode(wx.SOLID)
        dc.SetFont(self.font)
        
        
        ### Drawing servers: ##################################################
        #                                                                     #
        servers = state.servers
        
        for (i, server) in enumerate(servers):

            personality = server.personality
            
            name, light_color, dark_color = (
                personality.human_name,
                wx_tools.colors.rgb_to_wx_color(personality.light_color),
                wx_tools.colors.rgb_to_wx_color(personality.dark_color)
            )
            
            x0 = 10 + 200 * i
            y0 = 10
            
            pen = wx.Pen(light_color, 5)
            dc.SetPen(pen)
            
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            
            dc.DrawRectanglePointSize((x0, y0), (180, 50))
            
            dc.SetTextBackground(light_color)
            dc.SetTextForeground(dark_color)
                        
            dc.DrawText('Server %s' % name, x0, y0)
            
            client = server.current_client
            
            if client is None:
                dc.SetTextBackground('#d4d0c8')
                dc.SetTextForeground('#000000')
                dc.DrawText('Idle', x0 + 10, y0 + 22)
            
            else:
                
                client_personality = client.personality
                
                client_name, client_light_color, client_dark_color = (
                    client_personality.human_name,
                    wx_tools.colors.rgb_to_wx_color(client_personality.light_color),
                    wx_tools.colors.rgb_to_wx_color(client_personality.dark_color)
                )
                
                dc.SetTextBackground(client_light_color)
                dc.SetTextForeground(client_dark_color)
                dc.DrawText(client_name, x0 + 10, y0 + 22)
        #                                                                     #
        ### Finished drawing servers. #########################################
                
        
        ### Drawing population: ###############################################
        #                                                                     #
        assert state.population.size == infinity
        
        dc.SetTextBackground('#d4d0c8')
        dc.SetTextForeground('#000000')
        
        dc.DrawTextList(['Population:', 'Infinite'], [(10, 70), (10, 89)])
        #                                                                     #
        ### Finished drawing population. ######################################
        
        
        ### Drawing waiting clients: ##########################################
        #                                                                     #
        dc.SetTextBackground('#d4d0c8')
        dc.SetTextForeground('#000000')
        
        dc.DrawText('Clients in queue:', 150, 70)
        
        waiting_clients = state.facility.waiting_clients
        
        dc.DrawTextList(
            textList=
                [client.personality.human_name for client in waiting_clients],
            coords=
                [(150, 89 + (19 * i)) for i in range(len(waiting_clients))],
            foregrounds=
                [wx_tools.colors.rgb_to_wx_color(client.personality.dark_color) for
                 client in waiting_clients],
            backgrounds=
                [wx_tools.colors.rgb_to_wx_color(client.personality.light_color) for
                 client in waiting_clients]
        )
        #                                                                     #
        ### Finished drawing waiting clients. #################################
        

    def _on_size(self, event):
        self.Refresh()
        event.Skip()


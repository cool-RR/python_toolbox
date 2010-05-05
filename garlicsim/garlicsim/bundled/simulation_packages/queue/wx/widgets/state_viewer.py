# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the StateViewer class.

See its documentation for more information.
'''

import itertools

import wx
import wx.lib.scrolledpanel

import garlicsim
import garlicsim_wx
from garlicsim.general_misc.infinity import Infinity
from garlicsim_wx.general_misc import wx_tools


def make_wx_color((r, g, b)):
    return wx.Color(255*r, 255*g, 255*b)


class StateViewer(wx.lib.scrolledpanel.ScrolledPanel,
                  garlicsim_wx.widgets.WorkspaceWidget):
    '''Widget for showing a state of the `queue` simpack.'''
    def __init__(self, frame):
        wx.lib.scrolledpanel.ScrolledPanel.__init__(self, frame,
                                                    style=wx.SUNKEN_BORDER)
        garlicsim_wx.widgets.WorkspaceWidget.__init__(self, frame)
        
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        
        self.SetupScrolling()
        
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)
        #self.Bind(wx.EVT_MOUSE_EVENTS, self.on_mouse_event)
        
        self.state = None
        
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

    def on_paint(self, event):
        '''Paint event handler.'''
        
        event.Skip()
        
        state = self.state
        dc = wx.BufferedPaintDC(self)
        
        dc.SetBackground(wx_tools.get_background_brush())
        dc.Clear()
        
        if state is None:
            dc.Destroy()
            return
        
        dc.SetBackgroundMode(wx.SOLID)
        dc.SetFont(self.font)
        

        
        
        #######################################################################
        ############  Draw servers:
        #######################################################################

        servers = state.servers
        
        for (i, server) in enumerate(servers):

            personality = server.identity.get_personality()
            
            name, light_color, dark_color = (
                personality.human_name,
                make_wx_color(personality.light_color),
                make_wx_color(personality.dark_color)
            )
            
            x0 = 10 + 200 * i
            y0 = 10
            
            pen = wx.Pen(light_color, 5)
            dc.SetPen(pen)
            
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            
            dc.DrawRectanglePointSize((x0, y0), (180, 50))
            
            dc.SetTextBackground(light_color)
            dc.SetTextForeground(dark_color)
                        
            dc.DrawText('Server ' + name, x0, y0)
            
            client = server.current_client
            
            if client is None:
                dc.SetTextBackground('#d4d0c8')
                dc.SetTextForeground('#000000')
                dc.DrawText('Idle', x0 + 10, y0 + 22)
            
            else:
                
                client_personality = client.identity.get_personality()
                
                client_name, client_light_color, client_dark_color = (
                    client_personality.human_name,
                    make_wx_color(client_personality.light_color),
                    make_wx_color(client_personality.dark_color)
                )
                
                dc.SetTextBackground(client_light_color)
                dc.SetTextForeground(client_dark_color)
                dc.DrawText(client_name, x0 + 10, y0 + 22)
                
        
        
        
        #######################################################################
        ############  Draw population:
        #######################################################################

        assert state.population.size == Infinity
        
        dc.SetTextBackground('#d4d0c8')
        dc.SetTextForeground('#000000')
        
        dc.DrawTextList(['Population:', 'Infinite'], [(10, 70), (10, 89)])
        
        
        
        #######################################################################
        ############  Draw clients:
        #######################################################################
        
        dc.SetTextBackground('#d4d0c8')
        dc.SetTextForeground('#000000')
        
        dc.DrawText('Clients in queue:', 150, 70)
        
        personalities = [client.identity.get_personality() for client in
                         state.facility.waiting_clients]
        
        names = []; background_colors = []; foreground_colors = []
        
        for personality in personalities:
            names.append(personality.human_name)
            background_colors.append(make_wx_color(personality.light_color))
            foreground_colors.append(make_wx_color(personality.dark_color))
        
        coords = [(150, 89 + (19 * i)) for i in range(len(personalities))]
        
        dc.DrawTextList(names, coords, foreground_colors, background_colors)
        

        
        dc.Destroy()
        """

        self.SetVirtualSize(
            (
                board.width * (self.square_size + self.border_width),
                board.height * (self.square_size + self.border_width)
            )
        )
        """

    def on_size(self, event):
        '''Refresh the widget.'''
        self.Refresh()
        event.Skip()


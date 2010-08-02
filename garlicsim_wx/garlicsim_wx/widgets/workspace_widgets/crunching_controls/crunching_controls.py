# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.



import pkg_resources
import wx

from garlicsim_wx.general_misc.third_party import aui
from garlicsim_wx.general_misc import thread_timer
from garlicsim_wx.general_misc.flag_raiser import FlagRaiser
from garlicsim_wx.general_misc import emitters
from garlicsim_wx.widgets.general_misc import Knob

import garlicsim, garlicsim_wx
from garlicsim_wx.widgets import WorkspaceWidget
from scratch_wheel import ScratchWheel

from . import images as __images_package
images_package = __images_package.__name__

        

class CrunchingControls(wx.Panel, WorkspaceWidget):
    '''Widget to control playback of the simulation.'''
    
    _WorkspaceWidget__name = 'Crunching'

    def __init__(self, frame):
        wx.Panel.__init__(self, frame, -1, size=(184, 128),
                          style=wx.SUNKEN_BORDER)
        WorkspaceWidget.__init__(self, frame)
        
        #self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetBackgroundColour(wx.Color(212, 208, 200))
        
        assert isinstance(self.gui_project, garlicsim_wx.GuiProject)
        # I put this assert mainly for better source assistance in Wing.
        # It may be removed.
        
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        
        self.main_v_sizer = wx.BoxSizer(wx.VERTICAL)
        
        """
        self.inner_panel = wx.Panel(self, -1, size=(184, 124))
        '''The panel that contains all the subwidgets.'''
        
        self.inner_panel.SetBackgroundColour(wx.Color(212, 208, 200))
        
        self.center_button_mode = PlayMode
        '''The current mode of the center button.'''

        bitmap_list = ['to_start', 'previous_node', 'play',
                                'next_node', 'to_end', 'pause',
                                'finalize']
        
        bitmaps_dict = self.bitmap_dict = {}
        for bitmap_name in bitmap_list:
            stream = pkg_resources.resource_stream(images_package,
                                                 bitmap_name + '.png')
            self.bitmap_dict[bitmap_name] = wx.BitmapFromImage(
                wx.ImageFromStream(
                    stream,
                    wx.BITMAP_TYPE_ANY
                )
            )
            
        
        self.center_button_bitmap_dict = {
            PlayMode: bitmaps_dict['play'],
            PauseMode: bitmaps_dict['pause'],
            FinalizeMode: bitmaps_dict['finalize'],
            }
        

        v_sizer = self.v_sizer = wx.BoxSizer(wx.VERTICAL)


        playing_speed_getter = lambda: \
            self.gui_project.official_playing_speed / \
            self.gui_project.standard_playing_speed
        
        playing_speed_setter = lambda value: \
            self.gui_project.set_official_playing_speed(
                value * self.gui_project.standard_playing_speed
            )
        
        self.playing_speed_knob = Knob(
            self.inner_panel,
            getter = playing_speed_getter,
            setter = playing_speed_setter
        )
        '''Knob which controls the official playback speed.'''
        
        self.playing_speed_knob.set_snap_point(-1)
        self.playing_speed_knob.set_snap_point(1)
        
        
        self.knob_sizer = knob_sizer = wx.BoxSizer(wx.HORIZONTAL)
        knob_sizer.Add(
            self.playing_speed_knob,
            1,
            wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL |\
            wx.ALIGN_CENTER_VERTICAL | wx.LEFT,
            75
        )
        
        
        v_sizer.Add(
            knob_sizer, #self.playing_speed_knob, # knob_sizer,
            0,
            #wx.ALIGN_CENTER_HORIZONTAL #wx.EXPAND #|
        )


        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
                           
        self.button_to_start = wx.BitmapButton(
            self.inner_panel, -1, bitmaps_dict['to_start'], size=(31, 50)
        )
        '''Button for moving to start of path.'''
        
        self.button_previous_node = wx.BitmapButton(
            self.inner_panel, -1, bitmaps_dict['previous_node'], size=(31, 50)
        )
        '''Button for moving to previous node.'''
        
        self.button_center_button = wx.BitmapButton(
            self.inner_panel, -1, bitmaps_dict['play'], size=(60, 50)
        )
        '''Button for playing/pausing playback, and finalizing edited node.'''
        
        self.button_next_node= wx.BitmapButton(
            self.inner_panel, -1, bitmaps_dict['next_node'], size=(31, 50)
        )
        '''Button for moving to next node.'''
        
        self.button_to_end = wx.BitmapButton(
            self.inner_panel, -1, bitmaps_dict['to_end'], size=(31, 50)
        )
        '''Button for moving to end of path.'''
        
        
        self.Bind(wx.EVT_BUTTON, self.on_button_to_start,
                  source=self.button_to_start)
        
        self.Bind(wx.EVT_BUTTON, self.on_button_previous_node,
                  source=self.button_previous_node)
        
        self.Bind(wx.EVT_BUTTON, self.on_button_center_button,
                  source=self.button_center_button)
        
        self.Bind(wx.EVT_BUTTON, self.on_button_next_node,
                  source=self.button_next_node)
        
        self.Bind(wx.EVT_BUTTON, self.on_button_to_end,
                  source=self.button_to_end)
        
        button_line = (
            self.button_to_start,
            self.button_previous_node,
            self.button_center_button,
            self.button_next_node,
            self.button_to_end
        )
        
        for button in button_line:
            h_sizer.Add(button, 0)
        v_sizer.Add(h_sizer, 0)#1, wx.EXPAND)


        self.scratch_wheel = ScratchWheel(self.inner_panel, self.gui_project,
                                          -1, size=(184, 44))
        v_sizer.Add(self.scratch_wheel, 0)


        self.inner_panel.SetSizer(v_sizer)
        knob_sizer.Layout()
        h_sizer.Layout()
        v_sizer.Layout()
        
        
        self.center_button_update_flag = True
        '''Flag saying whether the center button needs update.'''
        
        self.navigation_buttons_update_flag = True
        '''Flag saying whether the navigation buttons need update.'''
        
        self.playing_speed_knob_update_flag = True
        '''Flag saying whether the playing speed knob needs update.'''
        
        self.center_button_needs_update_emitter = \
            self.gui_project.emitter_system.make_emitter(
                inputs=(
                    self.gui_project.playing_toggled_emitter,
                    self.gui_project.active_node_changed_or_modified_emitter,
                    self.gui_project.active_node_finalized_emitter
                ),
                outputs=(
                    FlagRaiser(self, 'center_button_update_flag',
                               function=self._update_center_button, delay=0.03),
                ),
                name='playback_controls_center_button_needs_update',
        )
        

        self.navigation_buttons_need_update_emitter = \
            self.gui_project.emitter_system.make_emitter(
                inputs=(
                    self.gui_project.active_node_changed_emitter,
                    self.gui_project.path_contents_changed_emitter
                ),            
                outputs=(
                    FlagRaiser(
                        self, 'navigation_buttons_update_flag',
                        function=self._update_navigation_buttons, delay=0.03
                        ),
                ),
                name='playback_controls_navigation_buttons_need_update',
        )
        
        
        self.gui_project.official_playing_speed_modified_emitter.add_output(
            FlagRaiser(self.playing_speed_knob, 'recalculation_flag',
                       self.playing_speed_knob._recalculate, delay=0.03)
        )
        """


    def on_size(self, event):
        '''EVT_SIZE handler.'''
        self.Refresh()
        event.Skip()
    
        
    def on_paint(self, event):
        '''EVT_PAINT handler.'''
        
        if self.center_button_update_flag:
            self._update_center_button()
        if self.navigation_buttons_update_flag:
            self._update_navigation_buttons()
        
        event.Skip()
        

    
# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
tododoc
'''

import pkg_resources
import wx

from garlicsim_wx.general_misc.third_party import aui
from garlicsim_wx.general_misc import thread_timer
from garlicsim_wx.general_misc.flag_raiser import FlagRaiser
from garlicsim_wx.general_misc import emitters

import garlicsim, garlicsim_wx
from garlicsim_wx.widgets import WorkspaceWidget
from garlicsim_wx.widgets.general_misc.knob import Knob

from scratch_wheel import ScratchWheel

from . import images as __images_package
images_package = __images_package.__name__

class CenterButtonMode(object):
    '''tododoc'''

class PlayMode(CenterButtonMode):
    '''tododoc'''
    @staticmethod
    def action(playback_controls):
        playback_controls.gui_project.start_playing()
    
class PauseMode(CenterButtonMode):
    @staticmethod
    def action(playback_controls):
        playback_controls.gui_project.stop_playing()
    
class FinalizeMode(CenterButtonMode):
    @staticmethod
    def action(playback_controls):
        try:
            playback_controls.gui_project.finalize_active_node()
        except Exception: # todo: should have meaningful exceptions all over
            pass


class PlaybackControls(wx.Panel, WorkspaceWidget):
    #DoGetBestSize = lambda self: wx.Size(184, 128)
    def __init__(self, frame):
        wx.Panel.__init__(self, frame, -1, size=(184, 128),
                          style=wx.SUNKEN_BORDER)
        WorkspaceWidget.__init__(self, frame)
        
        #self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        
        assert isinstance(self.gui_project, garlicsim_wx.GuiProject)
        # I put this assert mainly for better source assistance in Wing.
        # It may be removed.
        
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        """self.Bind(
            wx.EVT_IDLE,
            self.update_buttons_status,
        )
        # todo: eventually cancel this and use emitters
        """
        
        self.inner_panel = wx.Panel(self, -1, size=(184, 124))
        
        self.center_button_mode = PlayMode

        
        bitmap_list = ['to_start', 'previous_node', 'play',
                                'next_node', 'to_end', 'pause',
                                'finalize']
        
        bitmaps_dict = self.bitmap_dict = {}
        for bitmap_name in bitmap_list:
            path = pkg_resources.resource_filename(images_package,
                                                   bitmap_name + '.png')
            self.bitmap_dict[bitmap_name] = wx.Bitmap(path, wx.BITMAP_TYPE_ANY)
            
        
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
        self.button_previous_node = wx.BitmapButton(
            self.inner_panel, -1, bitmaps_dict['previous_node'], size=(31, 50)
        )
        self.button_center_button = wx.BitmapButton(
            self.inner_panel, -1, bitmaps_dict['play'], size=(60, 50)
        )
        self.button_next_node= wx.BitmapButton(
            self.inner_panel, -1, bitmaps_dict['next_node'], size=(31, 50)
        )
        self.button_to_end = wx.BitmapButton(
            self.inner_panel, -1, bitmaps_dict['to_end'], size=(31, 50)
        )
        
        
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
        self.navigation_buttons_update_flag = True
        self.playing_speed_knob_update_flag = True        
        
        self.center_button_needs_update_emitter = \
            self.gui_project.emitter_system.make_emitter(
                inputs=(
                    self.gui_project.playing_toggled_emitter,
                    self.gui_project.active_node_changed_emitter,
                    self.gui_project.active_node_finalized_emitter
                ),
                outputs=(
                    FlagRaiser(self, 'center_button_update_flag', delay=5),
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
                    FlagRaiser(self, 'navigation_buttons_update_flag', delay=5),
                ),
                name='playback_controls_navigation_buttons_need_update',
        )
        
        # todo: we might be doing here too many refreshes to ourselves. Remember
        # that a refresh on the PlaybackControls will refresh all its children,
        # which is expensive.
        
        self.gui_project.official_playing_speed_modified_emitter.add_output(
            FlagRaiser(self.playing_speed_knob, 'recalculation_flag')
        )


    def on_size(self, event):
        self.Refresh()
        event.Skip()
    
        
    def on_paint(self, event):
        
        if self.center_button_update_flag:
            self._update_center_button()
        if self.navigation_buttons_update_flag:
            self._update_navigation_buttons()
        
        event.Skip()
        
        # I thought I was supposed to call this here:
        # 
        # wx.Panel.OnPaint(self, event)
        # 
        # I don't, and for some reason this still works. Mysterious.
        

    def _update_navigation_buttons(self):
        
        active_node = self.gui_project.active_node
        
        if self.gui_project.path is None or active_node is None:
            self.button_to_start.Disable()
            self.button_previous_node.Disable()
            self.button_next_node.Disable()
            self.button_to_end.Disable()
    
        else:      
            if active_node.parent is not None:
                self.button_previous_node.Enable()
                self.button_to_start.Enable()
            else:
                self.button_previous_node.Disable()
                self.button_to_start.Disable()
                
            if active_node.children:
                self.button_next_node.Enable()
                self.button_to_end.Enable()
            else:
                self.button_next_node.Disable()
                self.button_to_end.Disable()
        
        self.navigation_buttons_update_flag = False    
        
    def _update_center_button(self):
        gui_project = self.gui_project
        active_node = gui_project.active_node
        
        if gui_project.path is None or active_node is None:
            self.set_center_button_mode(PlayMode)
            self.button_to_start.Disable()
        else:
            self.button_to_start.Enable()
            # todo: find out if it's wasteful to call enable if the button's
            # enbaled
            
            if active_node.still_in_editing:
                self.set_center_button_mode(FinalizeMode)
            elif self.gui_project.is_playing:
                self.set_center_button_mode(PauseMode)
            else: # self.gui_project.is_playing is False
                self.set_center_button_mode(PlayMode)
        
        self.center_button_update_flag = False
    
    def set_center_button_mode(self, center_button_mode): 
        # Not privatized because it's a setter
        if self.center_button_mode == center_button_mode:
            return
        self.button_center_button.SetBitmapLabel(
            self.center_button_bitmap_dict[center_button_mode]
        )
        self.center_button_mode = center_button_mode
       
        
    def on_button_to_start(self, e=None):
        try:
            if self.gui_project.path is None: return
            start_node = self.gui_project.path[0]
            self.gui_project.set_active_node(start_node)
        except garlicsim.data_structures.path.PathOutOfRangeError:
            return
        
    def on_button_to_end(self, e=None):
        try:
            if self.gui_project.path is None: return
            end_node = self.gui_project.path[-1]
            self.gui_project.set_active_node(end_node)
        except garlicsim.data_structures.path.PathOutOfRangeError:
            return
    
    def on_button_previous_node(self, e=None):
        if self.gui_project.active_node is None: return
        previous_node = self.gui_project.active_node.parent
        if previous_node is not None:
            self.gui_project.set_active_node(previous_node)
        
                
    def on_button_next_node(self, e=None):
        if self.gui_project.active_node is None: return
        try:
            next_node = \
                self.gui_project.path.next_node(self.gui_project.active_node)
            self.gui_project.set_active_node(next_node)
        except garlicsim.data_structures.path.PathOutOfRangeError:
            return
        
    def on_button_center_button(self, e=None):
        self.center_button_mode.action(self)
            
            
            
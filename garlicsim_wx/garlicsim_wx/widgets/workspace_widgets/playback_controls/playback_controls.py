# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `PlaybackControls` class.

See its documentation for more info.
'''

import pkg_resources
import wx

import garlicsim_wx.widgets.general_misc.cute_panel
from garlicsim_wx.general_misc.third_party import aui
from garlicsim_wx.general_misc import thread_timer
from garlicsim_wx.general_misc.flag_raiser import FlagRaiser
from garlicsim_wx.general_misc import emitters
from garlicsim_wx.general_misc import wx_tools
from garlicsim_wx.widgets.general_misc.knob import Knob
from garlicsim_wx.widgets.general_misc.cute_panel import CutePanel

import garlicsim, garlicsim_wx
from garlicsim_wx.widgets import WorkspaceWidget
from .scratch_wheel import ScratchWheel

from . import images as __images_package
images_package = __images_package.__name__


class CenterButtonMode(object):
    '''A mode that the center button can be in.'''
    

class PlayMode(CenterButtonMode):
    '''A mode in which pressing will cause playback to start.'''

    @staticmethod
    def action(playback_controls):
        '''Start playback.'''
        playback_controls.gui_project.start_playing()

        
class PauseMode(CenterButtonMode):
    '''A mode in which pressing will cause playback to pause.'''

    @staticmethod
    def action(playback_controls):
        '''Pause playback.'''
        playback_controls.gui_project.stop_playing()

        
class FinalizeMode(CenterButtonMode):
    '''A mode in which pressing will finalize the node being currently edited.'''

    @staticmethod
    def action(playback_controls):
        '''Finalize the node being currently edited.'''
        try:
            playback_controls.gui_project.finalize_active_node()
        except Exception: # todo: should have meaningful exceptions all over
            pass

        

class PlaybackControls(CutePanel, WorkspaceWidget):
    '''Widget to control playback of the simulation.'''
    
    _WorkspaceWidget__name = 'Playback'

    def __init__(self, frame):
        CutePanel.__init__(self, frame, -1, size=(184, 128),
                           style=wx.SUNKEN_BORDER)
        WorkspaceWidget.__init__(self, frame)
        
        #self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.set_good_background_color()
        self.SetDoubleBuffered(True)
        
        assert isinstance(self.gui_project, garlicsim_wx.GuiProject)
        
        self.inner_panel = \
            garlicsim_wx.widgets.general_misc.cute_panel.CutePanel(
                self,
                -1,
                size=(184, 124)
            )
        '''The panel that contains all the subwidgets.'''
        
        self.inner_panel.set_good_background_color()
        
        self.center_button_mode = PlayMode
        '''The current mode of the center button.'''

        bitmap_list = ['to_start', 'previous_node', 'play',
                       'next_node', 'to_end', 'pause', 'finalize']
        
        bitmaps_dict = self.bitmap_dict = {}
        for bitmap_name in bitmap_list:
            self.bitmap_dict[bitmap_name] = \
                wx_tools.bitmap_tools.bitmap_from_pkg_resources(
                    images_package,
                    bitmap_name + '.png'
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
        
                           
        self.start_button = wx.BitmapButton(
            self.inner_panel, -1, bitmaps_dict['to_start'], size=(31, 50)
        )
        '''Button for moving to start of path.'''
        
        self.previous_node_button = wx.BitmapButton(
            self.inner_panel, -1, bitmaps_dict['previous_node'], size=(31, 50)
        )
        '''Button for moving to previous node.'''
        
        self.center_button = wx.BitmapButton(
            self.inner_panel, -1, bitmaps_dict['play'], size=(60, 50)
        )
        '''Button for playing/pausing playback, and finalizing edited node.'''
        
        self.next_node_button= wx.BitmapButton(
            self.inner_panel, -1, bitmaps_dict['next_node'], size=(31, 50)
        )
        '''Button for moving to next node.'''
        
        self.end_button = wx.BitmapButton(
            self.inner_panel, -1, bitmaps_dict['to_end'], size=(31, 50)
        )
        '''Button for moving to end of path.'''
        
        self.bind_event_handlers(PlaybackControls)
        
        button_line = (
            self.start_button,
            self.previous_node_button,
            self.center_button,
            self.next_node_button,
            self.end_button
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

        
    def _update_navigation_buttons(self):
        '''Update the navigation buttons, disabling/enabling them as needed.'''
        
        active_node = self.gui_project.active_node
        
        if self.gui_project.path is None or active_node is None:
            self.start_button.Disable()
            self.previous_node_button.Disable()
            self.next_node_button.Disable()
            self.end_button.Disable()
    
        else:      
            if active_node.parent is not None:
                self.previous_node_button.Enable()
                self.start_button.Enable()
            else:
                self.previous_node_button.Disable()
                self.start_button.Disable()
                
            if active_node.children:
                self.next_node_button.Enable()
                self.end_button.Enable()
            else:
                self.next_node_button.Disable()
                self.end_button.Disable()
        
        self.navigation_buttons_update_flag = False    
       
        
    def _update_center_button(self):
        '''Update the center button, changing its mode if needed.'''
        gui_project = self.gui_project
        active_node = gui_project.active_node
        
        if gui_project.path is None or active_node is None:
            self.set_center_button_mode(PlayMode)
            self.start_button.Disable()
        else:
            self.start_button.Enable()
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
        '''Set the mode of the center button.'''
        # Not privatized because it's a setter
        if self.center_button_mode == center_button_mode:
            return
        self.center_button.SetBitmapLabel(
            self.center_button_bitmap_dict[center_button_mode]
        )
        self.center_button_mode = center_button_mode

        
    ### Event handlers: #######################################################
    #                                                                         #
    def _on_size(self, event):
        self.Refresh()
        event.Skip()
    
        
    def _on_paint(self, event):        
        if self.center_button_update_flag:
            self._update_center_button()
        if self.navigation_buttons_update_flag:
            self._update_navigation_buttons()
        
        event.Skip()
        
        
    def _on_start_button(self, event):
        try:
            if self.gui_project.path is None: return
            head_node = self.gui_project.path[0]
            self.gui_project.set_active_node(head_node)
        except garlicsim.data_structures.path.PathOutOfRangeError:
            return

        
    def _on_end_button(self, event):
        try:
            if self.gui_project.path is None: return
            tail_node = self.gui_project.path[-1]
            self.gui_project.set_active_node(tail_node)
        except garlicsim.data_structures.path.PathOutOfRangeError:
            return
    
    def _on_previous_node_button(self, event):
        if self.gui_project.active_node is None: return
        previous_node = self.gui_project.active_node.parent
        if previous_node is not None:
            self.gui_project.set_active_node(previous_node)
        
                
    def _on_next_node_button(self, event):
        if self.gui_project.active_node is None: return
        try:
            next_node = \
                self.gui_project.path.next_node(self.gui_project.active_node)
            self.gui_project.set_active_node(next_node)
        except garlicsim.data_structures.path.PathOutOfRangeError:
            return

        
    def _on_center_button(self, event):
        self.center_button_mode.action(self)
    #                                                                         #
    ### Finished event handlers. ##############################################
            
            
            
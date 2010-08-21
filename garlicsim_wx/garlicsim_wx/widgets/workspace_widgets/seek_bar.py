# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
This module defines the SeekBar class.

See its documentation for more info.
'''

import wx
import math

from garlicsim_wx.general_misc.get_lines import get_lines
from garlicsim_wx.general_misc import emitters
from garlicsim_wx.general_misc import wx_tools
from garlicsim_wx.general_misc.flag_raiser import FlagRaiser

from garlicsim_wx.widgets import WorkspaceWidget
import garlicsim
import garlicsim_wx


__all__ = ["SeekBar"]


class SeekBar(wx.Panel, WorkspaceWidget):
    '''
    Seek-bar widget, allowing navigation and visualization of the active path.
    
    The seek-bar is attached to a path. It shows what time period the path
    spans. It shows which node is currently active. It allows to move to any
    other node on the path just by clicking.
    '''
    #todo: show little breaks on the bar where there's a block start/end
    def __init__(self, frame):
        
        wx.Panel.__init__(self, frame, size=(100, 100), style=wx.SUNKEN_BORDER)
        WorkspaceWidget.__init__(self, frame)
        
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.on_mouse_event)

        self.zoom = 1.
        self.start = 0.

        self.screenify = lambda x: (x-self.start)*self.zoom
        '''Translate from time point to on-screen coordinate.'''
        
        self.unscreenify = lambda x: (x/self.zoom)+self.start
        '''Translate from on-screen coordinate to time point.'''
        
        self.menu = garlicsim_wx.general_misc.cute_menu.CuteMenu.add_menus(
            [garlicsim_wx.misc.menu_bar.node_menu.NodeMenu(self.frame),
             garlicsim_wx.misc.menu_bar.block_menu.BlockMenu(self.frame)]
        )

        self.was_playing_before_mouse_click = None
        self.was_playing_before_mouse_click_but_then_paused_and_mouse_left = None
        self.active_triangle_width = 13 # Must be odd number

        self.view_changed_flag = False
        self.active_node_changed_or_modified_flag = False
        self.path_contents_changed_flag = False
        
        self.view_change_emitter = emitters.Emitter()
        self.gui_project.active_node_changed_or_modified_emitter.add_output(
            FlagRaiser(self, 'active_node_changed_or_modified_flag')
        )
        self.gui_project.path_contents_changed_emitter.add_output(
            FlagRaiser(self, 'path_contents_changed_flag')
        )


    def on_paint(self, event):
        '''Refresh the seek-bar.'''
        event.Skip()
        

        self.view_changed_flag = False
        self.active_node_changed_or_modified_flag = False
        self.path_contents_changed_flag = False
        # todo: now we just lower these flags retardedly, in future there will
        # be __recalculate
        
        occupied_region = wx.Region()

        if (self.gui_project is None) or (self.gui_project.path is None):
            return
        
        (w, h) = self.GetSize()
        start = self.start
        end = self.start + (w / self.zoom)
        dc = wx.BufferedPaintDC(self)

        dc.SetBackground(wx_tools.get_background_brush())
        dc.Clear()
        
        #dc.DrawRectangle(3,3,50,90)
        if self.gui_project.path is not None: # Draw rect for renedered segment
            seg = self.gui_project.path.get_existing_time_segment(start, end)
            if seg is not None:
                dc.SetPen(wx.Pen('#000000'))
                dc.SetBrush(wx.Brush('#FFFFB8'))
                sseg = [self.screenify(thing) for thing in seg]
                dc.DrawRectangle(sseg[0], 0, sseg[1]-sseg[0], h-4)
                occupied_region = wx.Region(sseg[0] + 1, 1,
                                            sseg[1] - sseg[0] - 2,
                                            h - 6)

        active = self.gui_project.active_node
        if active is not None:
            active_start = active.state.clock
            try:
                after_active = self.gui_project.path.next_node(active)
                active_end = after_active.state.clock
            except garlicsim.data_structures.path.PathOutOfRangeError:
                after_active = None
                active_end = active_start
            active_inside = False
            screen_active_start = start
            screen_active_end = end

            if start <= active_start <= end:
                active_inside = True
                screen_active_start = self.screenify(active_start)

            if start <= active_end <= end:
                active_inside = True
                screen_active_end = self.screenify(active_end)


            dc.SetBrush(wx.Brush('#FF9933'))
            dc.SetPen(wx.Pen('#000000', 1, wx.TRANSPARENT))
            if active_inside is True:
                dc.DrawRectangle(math.floor(screen_active_start),
                                 1,
                                 math.ceil(screen_active_end-screen_active_start),
                                 h-6)
                triangle_half_width = math.ceil(self.active_triangle_width / 2.0)
                dc.SetClippingRegionAsRegion(occupied_region)
                dc.DrawPolygon(
                        ((screen_active_start - triangle_half_width, h - 5),
                        (screen_active_start + triangle_half_width, h - 5),
                        (screen_active_start, h - 5 - triangle_half_width))
                    )
                dc.DestroyClippingRegion()




        # Draw ruler
        min = 15
        temp = math.ceil(math.log10(min / self.zoom))
        bigliners = get_lines(start, end, temp+1)
        presmallliners = get_lines(start, end, temp)
        smallliners = []
        for thing in presmallliners:
            if bigliners.count(thing) == 0:
                smallliners.append(thing)

        self.draw_small_numbers(dc, smallliners)
        self.draw_big_numbers(dc, bigliners)
        
        dc.Destroy()


    def draw_small_numbers(self, dc, numbers):
        dc.SetPen(wx.Pen('#000000'))
        dc.SetFont(
            wx.Font(9,
                    wx.FONTFAMILY_DEFAULT,
                    wx.FONTSTYLE_NORMAL,
                    wx.FONTWEIGHT_NORMAL,
                    False,
                    'Courier 10 Pitch')
        )
        
        for number in numbers:
            dc.DrawLine(number, 0, number, 6)
            width, height = dc.GetTextExtent(str(number))
            dc.DrawText(str(number), (number - width / 2), 8)

    def draw_big_numbers(self, dc, numbers):
        dc.SetPen(wx.Pen('#000000'))
        dc.SetFont(
            wx.Font(9,
                    wx.FONTFAMILY_DEFAULT,
                    wx.FONTSTYLE_NORMAL,
                    wx.FONTWEIGHT_BOLD,
                    False,
                    'Courier 10 Pitch')
        )
        
        for number in numbers:
            dc.DrawLine(number, 0, number, 9)
            width, height = dc.GetTextExtent(str(number))
            dc.DrawText(str(number), (number - width / 2), 12)


    def on_mouse_event(self, e):
        #todo: should catch drag to outside of the window        
        # todo: use EVT_CONTEXT_MENU, in tree browser and others too
        if e.RightDown():
            self.gui_project.stop_playing()

            reselect_node = False
            new_thing = e.GetPositionTuple()[0]
            if self.gui_project.active_node is None:
                reselect_node=True
            else:
                thing = self.screenify(self.gui_project.active_node.state.clock)
                if abs(thing - new_thing) >= 8:
                    reselect_node = True

            if reselect_node is True:
                
                new_node = self.gui_project.path.get_node_occupying_timepoint \
                         (self.unscreenify(new_thing))
                
                if new_node is not None:
                    self.gui_project.set_active_node(new_node, modify_path=False)

            if self.gui_project.active_node is not None:
                self.gui_project.frame.Refresh()
                self.PopupMenu(self.menu, e.GetPosition())



        if e.LeftDClick():
            self.gui_project.toggle_playing()
            
        if e.LeftDown():# or e.RightDown():
            thing = e.GetPositionTuple()[0]
            node = self.gui_project.path.get_node_occupying_timepoint \
                 (self.unscreenify(thing))

            self.was_playing_before_mouse_click = self.gui_project.is_playing
            if self.was_playing_before_mouse_click:
                self.gui_project.stop_playing()

            if node is not None:
                self.gui_project.set_active_node(node, modify_path=False)


        if e.LeftIsDown():
            thing = e.GetPositionTuple()[0]
            node = self.gui_project.path.get_node_occupying_timepoint \
                 (self.unscreenify(thing))
            if node is not None:
                self.gui_project.set_active_node(node, modify_path=False)
                
        if e.LeftUp():
            if self.was_playing_before_mouse_click:
                self.gui_project.start_playing()
                self.was_playing_before_mouse_click = False
                
        if e.Leaving():
            if self.was_playing_before_mouse_click:
                self.gui_project.start_playing()
                self.was_playing_before_mouse_click = False
                self.was_playing_before_mouse_click_but_then_paused_and_mouse_left = True
                
        if e.Entering():
            if self.was_playing_before_mouse_click_but_then_paused_and_mouse_left:
                self.gui_project.stop_playing()
                self.was_playing_before_mouse_click = True
                self.was_playing_before_mouse_click_but_then_paused_and_mouse_left = False


    def on_size(self, e):
        self.Refresh()
        if e is not None:
            e.Skip()

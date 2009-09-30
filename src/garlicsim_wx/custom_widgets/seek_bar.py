# Copyright 2009 Ram Rachum.
# This program is not licensed for distribution and may not be distributed.

"""
todo: I think the refresh should be made more efficient

"""

import wx
import math
from garlicsim_wx.misc.getlines import get_lines
import garlicsim




class SeekBar(wx.Panel):
    """
    A seek-bar widget.
    """
    def __init__(self,parent,id,gui_project=None,zoom=1.0,start=0.0,*args,**kwargs):
        wx.Panel.__init__(self, parent, id, size=(-1,40), style=wx.SUNKEN_BORDER)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.on_mouse_event)

        self.gui_project=gui_project
        self.zoom=float(zoom)
        self.start=float(start)

        self.screenify=lambda x: (x-self.start)*self.zoom
        self.unscreenify=lambda x: (x/self.zoom)+self.start


        self.was_playing_before_mouse_click=None
        self.was_playing_before_mouse_click_but_then_paused_and_mouse_left=None
        self.active_triangle_width=13 # Must be odd number




    def OnPaint(self,e):
        occupied_region=wx.Region()

        if self.gui_project==None or self.gui_project.path==None:
            return
        (w,h)=self.GetSize()
        start=self.start
        end=self.start+w/self.zoom
        dc = wx.PaintDC(self)
        #dc.DrawRectangle(3,3,50,90)
        if self.gui_project.path!=None: #Draw rectangle for renedered segments
            seg=self.gui_project.path.get_existing_time_segment(start,end)
            if seg is not None:
                dc.SetPen(wx.Pen('#000000'))
                dc.SetBrush(wx.Brush('#FFFFB8'))
                sseg=[self.screenify(thing) for thing in seg]
                dc.DrawRectangle(sseg[0],0,sseg[1]-sseg[0],h-4)
                occupied_region=wx.Region(sseg[0]+1,1,sseg[1]-sseg[0]-2,h-4-2)

        active=self.gui_project.active_node
        if active!=None:
            active_start=active.state.clock
            try:
                after_active=self.gui_project.path.next_node(active)
                active_end=after_active.state.clock
            except garlicsim.data_structures.path.PathOutOfRangeError:
                after_active=None
                active_end=active_start
            active_inside=False
            screen_active_start=start
            screen_active_end=end


            if start<=active_start<=end:
                active_inside=True
                screen_active_start=self.screenify(active_start)

            if start<=active_end<=end:
                active_inside=True
                screen_active_end=self.screenify(active_end)


            dc.SetBrush(wx.Brush('#FF9933'))
            dc.SetPen(wx.Pen('#000000', 1, wx.TRANSPARENT))
            if active_inside==True:
                dc.DrawRectangle(math.floor(screen_active_start),1,math.ceil(screen_active_end-screen_active_start),h-6)
                triangle_half_width=math.ceil(self.active_triangle_width/2.0)
                dc.SetClippingRegionAsRegion(occupied_region)
                dc.DrawPolygon(((screen_active_start-triangle_half_width,h-5),(screen_active_start+triangle_half_width,h-5),(screen_active_start,h-5-triangle_half_width)))
                dc.DestroyClippingRegion()




        #Draw ruler
        min=15
        temp=math.ceil(math.log10(min/self.zoom))
        bigliners=get_lines(start,end,temp+1)
        presmallliners=get_lines(start,end,temp)
        smallliners=[]
        for thing in presmallliners:
            if bigliners.count(thing)==0:
                smallliners+=[thing]



        self.draw_small_numbers(dc,smallliners)
        self.draw_big_numbers(dc,bigliners)




    def draw_small_numbers(self,dc,numbers):
        dc.SetPen(wx.Pen('#000000'))
        dc.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, 'Courier 10 Pitch'))
        for number in numbers:
            dc.DrawLine(number, 0, number, 6)
            width, height = dc.GetTextExtent(str(number))
            dc.DrawText(str(number), number-width/2, 8)

    def draw_big_numbers(self,dc,numbers):
        dc.SetPen(wx.Pen('#000000'))
        dc.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, 'Courier 10 Pitch'))
        for number in numbers:
            dc.DrawLine(number, 0, number, 9)
            width, height = dc.GetTextExtent(str(number))
            dc.DrawText(str(number), number-width/2, 12)


    def on_mouse_event(self,e):
        #print(dir(e))
        if e.RightDown():
            self.gui_project.stop_playing()

            reselect_node=False
            new_thing=e.GetPositionTuple()[0]
            if self.gui_project.active_node==None:
                reselect_node=True
            else:
                thing=self.screenify(self.gui_project.active_node.state.clock)
                if abs(thing-new_thing)>=8:
                    reselect_node=True

            if reselect_node==True:
                new_node=self.gui_project.path.get_node_occupying_timepoint(self.unscreenify(new_thing))
                if new_node!=None:
                    self.gui_project.set_active_node(new_node,modify_path=False)

            if self.gui_project.active_node!=None:
                self.gui_project.main_window.Refresh()
                self.PopupMenu(self.gui_project.get_node_menu(), e.GetPosition())



        if e.LeftDClick():
            self.gui_project.toggle_playing()
        if e.LeftDown():# or e.RightDown():
            thing=e.GetPositionTuple()[0]
            node=self.gui_project.path.get_node_occupying_timepoint(self.unscreenify(thing))

            self.was_playing_before_mouse_click=self.gui_project.is_playing
            if self.was_playing_before_mouse_click:
                self.gui_project.stop_playing()

            if node!=None:
                self.gui_project.set_active_node(node,modify_path=False)


        if e.LeftIsDown():
            thing=e.GetPositionTuple()[0]
            node=self.gui_project.path.get_node_occupying_timepoint(self.unscreenify(thing))
            if node!=None:
                self.gui_project.set_active_node(node,modify_path=False)
        if e.LeftUp():
            if self.was_playing_before_mouse_click:
                self.gui_project.start_playing()
                self.was_playing_before_mouse_click=False
        if e.Leaving():
            if self.was_playing_before_mouse_click:
                self.gui_project.start_playing()
                self.was_playing_before_mouse_click=False
                self.was_playing_before_mouse_click_but_then_paused_and_mouse_left=True
        if e.Entering():
            if self.was_playing_before_mouse_click_but_then_paused_and_mouse_left:
                self.gui_project.stop_playing()
                self.was_playing_before_mouse_click=True
                self.was_playing_before_mouse_click_but_then_paused_and_mouse_left=False


    def OnSize(self,e):
        self.Refresh()

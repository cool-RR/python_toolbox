import wx
import math
from misc.getlines import get_lines as get_lines




class Timeline(wx.Panel):
    def __init__(self,parent,id,gui_project=None,zoom=1.0,start=0.0,*args,**kwargs):
        wx.Panel.__init__(self, parent, id, size=(-1,40), style=wx.SUNKEN_BORDER)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.gui_project=gui_project
        self.zoom=float(zoom)
        self.start=float(start)

        self.screenify=lambda x: (x-self.start)*self.zoom
        self.unscreenify=lambda x: (x/self.zoom)+self.start
        self.Bind(wx.EVT_MOUSE_EVENTS, self.on_mouse_event)


        self.was_playing_before_mouse_click=None
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
            segs=self.gui_project.path.get_rendered_segments(start,end)
            dc.SetPen(wx.Pen('#000000'))
            dc.SetBrush(wx.Brush('#FFFFB8'))
            for seg in segs:
                sseg=[self.screenify(thing) for thing in seg]
                dc.DrawRectangle(sseg[0],0,sseg[1]-sseg[0],h-4)
                occupied_region=wx.Region(sseg[0]+1,1,sseg[1]-sseg[0]-2,h-4-2)

        active=self.gui_project.active_node
        if active!=None:
            active_start=active.state.clock
            try:
                after_active=self.gui_project.path.next_node(active)
                active_end=after_active.state.clock
            except IndexError:
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
        if e.LeftDClick():
            self.gui_project.toggle_playing()
        if e.LeftDown():
            thing=e.GetPositionTuple()[0]
            node=self.gui_project.path.get_node_by_time(self.unscreenify(thing))

            self.was_playing_before_mouse_click=self.gui_project.is_playing
            if self.was_playing_before_mouse_click:
                self.gui_project.stop_playing()

            if node!=None:
                self.gui_project.make_active_node(node)


        if e.LeftIsDown():
            thing=e.GetPositionTuple()[0]
            node=self.gui_project.path.get_node_by_time(self.unscreenify(thing))
            if node!=None:
                self.gui_project.make_active_node(node)
        if e.LeftUp():
            if self.was_playing_before_mouse_click:
                self.gui_project.start_playing()
                self.was_playing_before_mouse_click=False
        if e.Leaving():
            if self.was_playing_before_mouse_click:
                self.gui_project.start_playing()
                self.was_playing_before_mouse_click=False



    def OnSize(self,e):
        self.Refresh()

if __name__=="__main__":

    class ShoobiFrame(wx.Frame):
        def __init__(self,*args,**kwargs):
            wx.Frame.__init__(self,*args,**kwargs)
            self.sizer=wx.BoxSizer(wx.VERTICAL)
            self.text1=wx.TextCtrl(self, -1, style=wx.TE_MULTILINE)
            self.text2=wx.TextCtrl(self, -1, style=wx.TE_MULTILINE)
            self.timeline=Timeline(self,-1)
            self.sizer.Add(self.text1,1,wx.EXPAND)
            self.sizer.Add(self.timeline,1,wx.EXPAND)
            self.sizer.Add(self.text2,1,wx.EXPAND)
            self.SetSizer(self.sizer)
            self.Show()

    app = wx.PySimpleApp()
    shoobi=ShoobiFrame(None,-1,"Title",size=(600,600))
    app.MainLoop()
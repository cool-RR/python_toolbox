import wx
import math
from misc.getlines import get_lines as get_lines

class Timeline(wx.Panel):
    def __init__(self,parent,id,gui_project=None,path=None,zoom=1.0,start=0.0,*args,**kwargs):
        wx.Panel.__init__(self, parent, id, size=(-1,100), style=wx.SUNKEN_BORDER)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.path=path
        self.gui_project=gui_project
        self.zoom=float(zoom)
        self.start=float(start)

        self.screenify=lambda x: (x-self.start)*self.zoom
        self.unscreenify=lambda x: (x/self.zoom)+self.start
        self.Bind(wx.EVT_MOUSE_EVENTS, self.on_mouse_event)




    def OnPaint(self,e):
        if self.gui_project==None or self.path==None:
            return
        (w,h)=self.GetSize()
        start=self.start
        end=self.start+w/self.zoom
        dc = wx.PaintDC(self)
        #dc.DrawRectangle(3,3,50,90)
        if self.path!=None: #Draw rectangle for renedered segments
            segs=self.path.get_rendered_segments(start,end)
            dc.SetPen(wx.Pen('#000000'))
            dc.SetBrush(wx.Brush('#FFFFB8'))
            for seg in segs:
                dc.DrawRectangle(self.screenify(seg[0]),0,self.screenify(seg[1]-seg[0]),h-4)

        active=self.gui_project.active_node
        if active!=None:
            active_start=active.state.clock
            try:
                after_active=self.path.next_node(active)
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



            if active_inside==True:
                dc.SetBrush(wx.Brush('#FF9933'))
                dc.SetPen(wx.Pen('#000000', 1, wx.TRANSPARENT))
                dc.DrawRectangle(math.floor(screen_active_start),1,math.ceil(screen_active_end-screen_active_start),h-6)





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
        if e.LeftUp():
            thing=e.GetPositionTuple()[0]
            node=self.path.get_node_by_time(self.unscreenify(thing))
            if node!=None:
                self.gui_project.make_active_node(node)


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
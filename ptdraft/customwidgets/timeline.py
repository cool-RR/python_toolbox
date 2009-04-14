import wx
import math
from misc.getlines import get_lines as get_lines

class Timeline(wx.Panel):
    def __init__(self,parent,id,*args,**kwargs):
        wx.Panel.__init__(self, parent, id, size=(-1,100), style=wx.SUNKEN_BORDER)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        try:
            self.zoom=float(kwargs["zoom"])
        except:
            self.zoom=1.0

        try:
            self.start=float(kwargs["start"])
        except:
            self.start=0.0

        try:
            self.path=kwargs["path"]
        except:
            self.path=None

    def set_path(self,path):
        self.path=path

    def OnPaint(self,e):
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
                dc.DrawRectangle((seg[0]-self.start)*self.zoom,0,(seg[1]-self.start)*self.zoom,h-4)

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
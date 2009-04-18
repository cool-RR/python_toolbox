import wx
from math import *
import misc.vectorish as vectorish
from state import *

connector_length=10 #length of connecting line between elements


class NiftyPaintDC(wx.PaintDC):
    elements={  \
                   "Untouched": wx.Bitmap("images\\graycircle.png", wx.BITMAP_TYPE_ANY),    \
                   "Touched": wx.Bitmap("images\\graystar.png", wx.BITMAP_TYPE_ANY),    \
                   "Block": wx.Bitmap("images\\grayblock.png", wx.BITMAP_TYPE_ANY),    \
                   "Selected Untouched": wx.Bitmap("images\\bluecircle.png", wx.BITMAP_TYPE_ANY),    \
                   "Selected Touched": wx.Bitmap("images\\bluestar.png", wx.BITMAP_TYPE_ANY),    \
                   "Selected Block": wx.Bitmap("images\\blueblock.png", wx.BITMAP_TYPE_ANY),    \
                   }

    def draw_sub_tree(self,point,tree,start):
        if isinstance(start,Block):
            type="Block"
            kids=start[-1].children
        elif isinstance(start,Node):
            kids=start.children
            if start.state.is_touched()==True:
                type="Touched"
            else:
                type="Untouched"
        else:
            raise StandardError

        if False: # todo: if it's selected
            type="Selected "+type

        bitmap=self.elements[type]
        self.DrawBitmapPoint(bitmap,point,useMask=True)
        bitmap_size=bitmap.GetSize()

        last_height=0
        total_height=0
        self_width=bitmap_size[0]+connector_length
        max_width=self_width
        line_start=vectorish.add(point,(bitmap_size[0]-1,bitmap_size[1]//2))

        for kid in kids:
            line_end=vectorish.add(point,(self_width+1,total_height+bitmap_size[1]//2))
            (new_width,new_height)=self.draw_sub_tree(vectorish.add(point,(self_width,total_height)),tree,kid.soft_get_block())
            self.DrawLinePoint(line_start,line_end)
            max_width=max(max_width,new_width)
            total_height+=new_height

        return (max_width,max(total_height,bitmap_size[1]+connector_length))

    def draw_tree(self,tree):
        """
        assuming the tree has only one root!
        """
        size=self.draw_sub_tree((connector_length,connector_length),tree,tree.roots[0].soft_get_block())
        (width,height)=vectorish.add(size,(connector_length,connector_length))
        return (width,height)




class TreeBrowser(wx.ScrolledWindow):
    def __init__(self,parent,id,*args,**kwargs):
        wx.ScrolledWindow.__init__(self, parent, id, size=(-1,200),style=wx.SUNKEN_BORDER)
        self.SetScrollRate(20,20)
        #self.sizer=wx.BoxSizer(wx.VERTICAL)
        #self.panel=wx.StaticBitmap(self,-1,wx.Bitmap("images\\snail.gif", wx.BITMAP_TYPE_ANY))#wx.Panel(self,-1,size=(-1,200))#wx.TextCtrl(self, -1, size=(-1,200), style=wx.TE_MULTILINE)
        self.panel=wx.Panel(self,-1,size=(200,200))#wx.TextCtrl(self, -1, size=(-1,200), style=wx.TE_MULTILINE)
        #self.sizer.Add(self.panel,0)
        #self.SetSizer(self.sizer)
        #self.EnableScrolling(True, True)
        #self.SetScrollbars(5, 30, 1055, 40)
        #self.sizer.Fit(self)
        #self.Centre()
        #self.SetVirtualSize((1000,1000))

        self.panel.Bind(wx.EVT_PAINT, self.OnPaint)
        self.panel.Bind(wx.EVT_SIZE, self.OnSize)

        try:
            self.tree=kwargs["tree"]
        except:
            self.tree=None

    def set_tree(self,tree):
        self.tree=tree

    def OnPaint(self,e):


        pen=wx.Pen("Black",1,wx.SOLID)
        pen.SetCap(wx.CAP_PROJECTING)
        pen.SetJoin(wx.JOIN_ROUND)
        dc = NiftyPaintDC(self.panel)
        (width,height)=dc.draw_tree(self.tree)
        self.SetVirtualSize((width,height))


    def OnSize(self,e):
        self.Refresh()

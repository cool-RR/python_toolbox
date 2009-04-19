import wx
from math import *
import misc.vectorish as vectorish
from state import *

connector_length=10 #length of connecting line between elements


class NiftyPaintDC(wx.PaintDC):
    def __init__(self,window,gui_project,*args,**kwargs):
        wx.PaintDC.__init__(self,window,*args,**kwargs)
        self.gui_project=gui_project

    elements={  \
                   "Untouched": wx.Bitmap("images\\graysquare.png", wx.BITMAP_TYPE_ANY),    \
                   "Touched": wx.Bitmap("images\\graystar.png", wx.BITMAP_TYPE_ANY),    \
                   "Block": wx.Bitmap("images\\grayblock.png", wx.BITMAP_TYPE_ANY),    \
                   "Selected Untouched": wx.Bitmap("images\\bluesquare.png", wx.BITMAP_TYPE_ANY),    \
                   "Selected Touched": wx.Bitmap("images\\bluestar.png", wx.BITMAP_TYPE_ANY),    \
                   "Selected Block": wx.Bitmap("images\\blueblock.png", wx.BITMAP_TYPE_ANY),    \
                   "Active Untouched": wx.Bitmap("images\\orangesquare.png", wx.BITMAP_TYPE_ANY),    \
                   "Active Touched": wx.Bitmap("images\\orangestar.png", wx.BITMAP_TYPE_ANY),    \
                   "Active Block": wx.Bitmap("images\\orangeblock.png", wx.BITMAP_TYPE_ANY),    \
                   }

    def draw_sub_tree(self,point,tree,start):
        make_block_stripe=False
        if isinstance(start,Block):
            type="Block"
            kids=start[-1].children
            if start==self.active_soft_block:
                make_block_stripe=True
                type="Active "+type
        elif isinstance(start,Node):
            kids=start.children
            if start.state.is_touched()==True:
                type="Touched"
            else:
                type="Untouched"
            if start==self.active_soft_block:
                type="Active "+type
        else:
            raise StandardError

        if False: # todo: if it's selected
            type="Selected "+type

        if make_block_stripe==True:

            bitmap=self.elements["Block"]
            self.DrawBitmapPoint(bitmap,point,useMask=True)
            bitmap_size=bitmap.GetSize()
            second_bitmap=self.elements[type]

            slice=[None,None]
            length=float(len(start.list))
            slice[0]=start.list.index(self.active_node)/length
            slice[1]=slice[0]+1/length

            screen_slice=[floor(point[0]+2+(bitmap_size[0]-4)*slice[0]),ceil(point[0]+2+(bitmap_size[0]-4)*slice[1])]
            region=wx.Region(screen_slice[0],point[1],screen_slice[1]-screen_slice[0],bitmap_size[1])
            self.SetClippingRegionAsRegion(region)
            self.DrawBitmapPoint(second_bitmap,point,useMask=True)
            self.DestroyClippingRegion()




        else:
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
        self.active_node=self.gui_project.active_node
        try:
            self.active_soft_block=self.active_node.soft_get_block()
        except AttributeError:
            self.active_soft_block=None
        size=self.draw_sub_tree((connector_length,connector_length),tree,tree.roots[0].soft_get_block())
        (width,height)=vectorish.add(size,(connector_length,connector_length))
        return (width,height)




class TreeBrowser(wx.ScrolledWindow):
    def __init__(self,parent,id,gui_project=None,tree=None,*args,**kwargs):
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

        self.tree=tree
        self.gui_project=gui_project


    def OnPaint(self,e):
        if self.gui_project==None or self.tree==None:
            return


        pen=wx.Pen("Black",1,wx.SOLID)
        pen.SetCap(wx.CAP_PROJECTING)
        pen.SetJoin(wx.JOIN_ROUND)
        dc = NiftyPaintDC(self.panel,self.gui_project)
        (width,height)=dc.draw_tree(self.tree)
        self.SetVirtualSize((width,height))


    def OnSize(self,e):
        self.Refresh()

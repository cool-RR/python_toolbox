import wx
import os
from misc import s2i,i2s
import time

from core import *
import simulations.life.life as life
import simulations.life.lifegui as lifegui


class myframe(wx.Frame):
    def __init__(self,*args,**keywords):
        wx.Frame.__init__(self,*args,**keywords)
        self.nibicon=wx.Bitmap("images\\circle.png", wx.BITMAP_TYPE_ANY)
        self.touchednibicon=wx.Bitmap("images\\star.png", wx.BITMAP_TYPE_ANY)

        filemenu=wx.Menu()
        filemenu.Append(s2i("Open"),"&Open"," Open a file")
        filemenu.AppendSeparator()
        filemenu.Append(s2i("Exit"),"E&xit"," Close the program")

        stuffmenu=wx.Menu()
        stuffmenu.Append(s2i("Calculate"),"&Calculate","")
        stuffmenu.Append(s2i("Play"),"&Play","")


        wx.EVT_MENU(self,s2i("Exit"),self.exit)

        wx.EVT_MENU(self,s2i("Calculate"),self.calculate)
        wx.EVT_MENU(self,s2i("Play"),self.play)



        menubar=wx.MenuBar()
        menubar.Append(filemenu,"&File")
        menubar.Append(stuffmenu,"&Stuff")
        self.SetMenuBar(menubar)
        self.CreateStatusBar()
        toolbar = self.CreateToolBar()
        toolbar.AddSimpleTool(s2i("Button New"), wx.Bitmap("images\\new.png", wx.BITMAP_TYPE_ANY),"New", " Create a new file")
        toolbar.AddSimpleTool(s2i("Button Open"), wx.Bitmap("images\\open.png", wx.BITMAP_TYPE_ANY),"Open", " Open a file")
        toolbar.AddSimpleTool(s2i("Button Save"), wx.Bitmap("images\\save.png", wx.BITMAP_TYPE_ANY),"Save", " Save to file")
        toolbar.Realize()

        self.thing=wx.ScrolledWindow(self,-1)




        self.sizer=wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.thing,1,wx.EXPAND)


        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        #self.sizer.Fit(self)

        #self.Bind(wx.EVT_PAINT, self.draw)

        self.Show()
        #self.draw()

        self.mygui=lifegui.LifeGuiPlayon(Playon(life.Life),self.thing)
        self.root=self.mygui.playon.makerandomroot(30,30)

    def calculate(self,e):
        try:
            self.deus=self.tres
        except:
            self.deus=self.tres=self.root

        self.tres=self.mygui.playon.multistep(self.deus,steps=200)

    def play(self,e):
        self.mygui.showstartend(self.deus,self.tres,0.1)


    def draw(self,e=None):
        pass
        """
        dc = wx.PaintDC(self.realthing)

        brush = wx.Brush("sky blue")
        dc.SetBackground(brush)
        dc.Clear()
        for i in range(100):
            dc.DrawBitmap(self.nibicon,10+20*i,10,True)
        self.realthing.SetVirtualSize((1000,1000))
        """


    def exit(self,e):
        self.Close()




    """
    def loadstring(self,*args,**kwargs):
        self.control.
    """


app = wx.PySimpleApp()
fugi=myframe(None,-1,"Title",size=(600,600))
app.MainLoop()
import wx
from misc.stringsaver import s2i,i2s
from core import *

class GuiPlayon(object):
    def __init__(self,myp,window):
        """
        I think that window is supposed to be a ScrolledWindow
        """
        self.playon=myp
        self.window=window

    def showstartend(self,start,end,delay):
        self.showmovie(self.playon.nibtree.getmovie(start,end), delay)

    def showmovie(self,movie,delay):
        self.shownib(movie[0].nib)
        if len(movie)>1:
            wx.FutureCall(delay*1000,functools.partial(self.showmovie,movie[1:],delay))

    def playpath(self,path,delay):
        if path.start==None:
            return None
        self.shownib(path.start.nib)
        wx.FutureCall(delay*1000,functools.partial(self.playpath,path.cutofffirst(),delay))


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

    def show_start_end(self,start,end,delay):
        self.show_movie(self.playon.nibtree.get_movie(start,end), delay)

    def show_movie(self,movie,delay):
        self.show_nib(movie[0].nib)
        if len(movie)>1:
            wx.FutureCall(delay*1000,functools.partial(self.show_movie,movie[1:],delay))

    def play_path(self,path,delay):
        if path.start==None:
            return None
        self.show_nib(path.start.nib)
        wx.FutureCall(delay*1000,functools.partial(self.play_path,path.cut_off_first(),delay))


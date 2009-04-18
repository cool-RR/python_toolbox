import wx
from misc.stringsaver import s2i,i2s
from core import *

class GuiProject(object):
    def __init__(self,project,window):
        """
        I think that window is supposed to be a ScrolledWindow
        """
        self.project=project
        self.window=window

    def show_start_end(self,start,end,delay):
        self.show_movie(self.project.tree.get_movie(start,end), delay)

    def show_movie(self,movie,delay):
        self.show_state(movie[0].state)
        if len(movie)>1:
            wx.FutureCall(delay*1000,functools.partial(self.show_movie,movie[1:],delay))

    def play_path(self,path,delay):
        if path.start==None:
            return None
        self.show_state(path.start.state)
        wx.FutureCall(delay*1000,functools.partial(self.play_path,path.cut_off_first(),delay))


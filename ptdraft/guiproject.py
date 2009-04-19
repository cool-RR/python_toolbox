import wx
from misc.stringsaver import s2i,i2s
from core import *
import warnings

class GuiProject(object):
    def __init__(self,project,window):
        """
        I think that window is supposed to be a ScrolledWindow
        """
        self.project=project
        self.window=window

        self.active_node=None #This property contains the node that is currently displayed onscreen

        self.selected=None
        """
        This property will tell which nodes are "selected". I'm not sure how I'll implement this,
        maybe a NodeSelection class.
        """

        self.playing=False

        self.delay=0.05 # Should be a mechanism for setting that

        self.timer_for_playing=None

        self.path=None

    def make_active_node(self,node,assuring_no_jump=False):
        """
        Makes "node" the active node
        """
        was_playing=False
        if assuring_no_jump==False and self.playing==True:
            self.stop_playing()
            was_playing=True
        self.show_state(node.state)
        self.active_node=node
        if assuring_no_jump==False and was_playing==True:
            self.start_playing()

    def start_playing(self):
        self.playing=True
        self.play_next(self.active_node)
        print("boobs")


    def stop_playing(self):
        self.playing=False
        if self.timer_for_playing!=None:
            self.timer_for_playing.Stop()
        else:
            warnings.warn("Tried to stop playing though wasn't playing")


    def play_next(self,node):
        self.make_active_node(node,assuring_no_jump=True)
        self.timer_for_playing=wx.FutureCall(self.delay*1000,functools.partial(self.play_next,self.path.next_node(node)))


    def show_start_end(self,start,end,delay):
        self.show_movie(self.project.tree.get_movie(start,end), delay)

    def show_movie(self,movie,delay):
        self.show_state(movie[0].state)
        if len(movie)>1:
            wx.FutureCall(delay*1000,functools.partial(self.show_movie,movie[1:],delay))

    def play_path(self,path,delay):
        if path.start==None:
            return None
        self.make_active_node(path.start)
        wx.FutureCall(delay*1000,functools.partial(self.play_path,path.cut_off_first(),delay))


import wx
from misc.stringsaver import s2i,i2s
from core import *
import warnings
import customwidgets

class GuiProject(object):
    def __init__(self,project,parent_window):
        """
        I think that window is supposed to be a ScrolledWindow
        """
        self.project=project
        self.main_window=wx.ScrolledWindow(parent_window,-1)

        self.state_showing_window=wx.ScrolledWindow(self.main_window,-1)
        self.timeline=customwidgets.Timeline(self.main_window,-1,self)
        self.tree_browser=customwidgets.TreeBrowser(self.main_window,-1,self)

        self.sizer=wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.state_showing_window,1,wx.EXPAND)
        self.sizer.Add(self.timeline,0,wx.EXPAND)
        self.sizer.Add(self.tree_browser,0,wx.EXPAND)
        self.main_window.SetSizer(self.sizer)
        self.sizer.Fit(self.main_window)



        self.active_node=None #This property contains the node that is currently displayed onscreen

        self.selected=None
        """
        This property will tell which nodes are "selected". I'm not sure how I'll implement this,
        maybe a NodeSelection class.
        """

        self.is_playing=False

        self.delay=0.05 # Should be a mechanism for setting that
        self.default_buffer=50 # Should be a mechanism for setting that

        self.timer_for_playing=None

        self.paths=[]
        """
        Contains a list of paths
        """

        self.path=None
        """
        The active path
        """

        parent_window.Bind(wx.EVT_MENU,self.edit_from_active_node,id=s2i("Fork by editing"))
        parent_window.Bind(wx.EVT_MENU,self.step_from_active_node,id=s2i("Fork naturally"))

    def set_active_path(self,path):
        if not path in self.paths:
            self.paths.append(path)
        self.path=path

    def make_plain_root(self,*args,**kwargs):
        root=self.project.make_plain_root(*args,**kwargs)
        if self.path==None:
            self.path=state.Path(self.project.tree,root)
        else:
            self.path.start=root
        self.project.render_all_edges(root,self.default_buffer)
        return root

    def make_random_root(self,*args,**kwargs):
        root=self.project.make_random_root(*args,**kwargs)
        if self.path==None:
            self.path=state.Path(self.project.tree,root)
        else:
            self.path.start=root
        self.project.render_all_edges(root,self.default_buffer)
        return root

    def make_active_node_and_correct_path(self,node):
        self.make_active_node(node)
        if node in self.path:
            return
        else:
            current=node
            while True:
                parent=current.parent
                if parent==None:
                    self.path.start=current
                    break
                if len(parent.children)>1:
                    self.path.decisions[parent]=current
                current=parent

    def make_active_node(self,node):
        """
        Makes "node" the active node
        """
        self.project.render_all_edges(node,self.default_buffer)
        was_playing=False
        if self.is_playing==True:
            self.stop_playing()
            was_playing=True
        self.show_state(node.state)
        self.active_node=node
        if was_playing==True:
            self.start_playing()


    def start_playing(self):
        if self.is_playing==True:
            return
        if self.active_node==None:
            return

        edge=self.project.get_edge_on_path(self.active_node,None,self.path).popitem()[0]
        if self.project.edges_to_render.has_key(edge):
            self.was_buffering_before_starting_to_play=True
            self.edge_and_buffering_amount_before_starting_to_play=(edge,self.project.edges_to_render[edge])
        else:
            self.was_buffering_before_starting_to_play=False

        self.project.edges_to_render[edge]=None

        self.is_playing=True
        self.play_next(self.active_node)


    def stop_playing(self):
        if self.is_playing==False:
            return
        self.is_playing=False
        self.timer_for_playing.Stop()

        if self.was_buffering_before_starting_to_play:
            (old_edge,d)=self.edge_and_buffering_amount_before_starting_to_play
            current_edge=self.project.get_edge_on_path(self.active_node,None,self.path).popitem()[0]
            dist=self.path.distance_between_nodes(old_edge,current_edge)
            maximum=max(d-dist,self.default_buffer) if d!=None else None
            self.project.edges_to_render[current_edge]=maximum
            self.was_buffering_before_starting_to_play=False
        else:
            current_edge=self.project.get_edge_on_path(self.active_node,None,self.path).popitem()[0]
            self.project.edges_to_render[current_edge]=self.default_buffer



    def toggle_playing(self):
        if self.is_playing:
            return self.stop_playing()
        else:
            return self.start_playing()


    def play_next(self,node):
        self.show_state(node.state)
        self.active_node=node
        try:
            next_node=self.path.next_node(node)
        except IndexError:
            """
            Do something here that will continue playing,
            albeit slowly, when more nodes have been crunched
            """
            self.stop_playing()
            return
        self.timer_for_playing=wx.FutureCall(self.delay*1000,functools.partial(self.play_next,next_node))

    def step_from_active_node(self,*args,**kwargs):
        new_node=self.project.step(self.active_node)
        self.notify_paths_of_fork(self.active_node,new_node)
        self.project.render_all_edges(new_node,self.default_buffer)

    def edit_from_active_node(self,*args,**kwargs):
        pass

    def notify_paths_of_fork(self,parent_node,child_node):
        non_active_paths=[path for path in self.paths if path!=self.path]

        if self.path!=None:
            self.path.decisions[parent_node]=child_node
        for path in non_active_paths:
            if path.decisions.has_key(parent_node)==False:
                path.decisions[parent_node]=parent_node.children[0]


    def get_node_menu(self):
        nodemenu=wx.Menu()
        nodemenu.Append(s2i("Fork by editing"),"Fork by &editing"," Create a new edited node with the current node as the template")
        nodemenu.Append(s2i("Fork naturally"),"Fork &naturally"," Run the simulation from this node")
        nodemenu.AppendSeparator()
        nodemenu.Append(s2i("Delete..."),"&Delete..."," Delete the node")
        return nodemenu




    """

    def play_path(self,path,delay):
        if path.start==None:
            return None
        self.make_active_node(path.start)
        wx.FutureCall(delay*1000,functools.partial(self.play_path,path.cut_off_first(),delay))


    def show_start_end(self,start,end,delay):
        self.show_movie(self.project.tree.get_movie(start,end), delay)

    def show_movie(self,movie,delay):
        self.show_state(movie[0].state)
        if len(movie)>1:
            wx.FutureCall(delay*1000,functools.partial(self.show_movie,movie[1:],delay))
    """

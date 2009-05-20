import wx
import wx.lib.scrolledpanel as scrolled

import functools

from misc.stringsaver import s2i,i2s
from misc.infinity import Infinity
import garlicsim
import warnings

import copy

import customwidgets
FoldableWindowContainer=customwidgets.FoldableWindowContainer

import wx.py.shell


class GuiProject(object):
    """
    A GuiProject encapsulates a Project for use with a wxPython
    interface.
    """
    def __init__(self,simulation_package,parent_window):
        self.project=garlicsim.Project(simulation_package)



        main_window=self.main_window=wx.ScrolledWindow(parent_window,-1)
        self.main_sizer=wx.BoxSizer(wx.VERTICAL)
        self.main_window.SetSizer(self.main_sizer)

        self.state_showing_window=scrolled.ScrolledPanel(self.main_window,-1)

        self.shell=wx.py.shell.Shell(self.main_window,-1,size=(400,-1))
        self.seek_bar=customwidgets.SeekBar(self.main_window,-1,self)
        self.tree_browser=customwidgets.TreeBrowser(self.main_window,-1,self)


        self.top_fwc=FoldableWindowContainer(self.main_window,-1,self.state_showing_window,self.shell,wx.RIGHT,folded=True)
        temp=FoldableWindowContainer(self.main_window,-1,self.top_fwc,self.seek_bar,wx.BOTTOM)
        temp=FoldableWindowContainer(self.main_window,-1,temp,self.tree_browser,wx.BOTTOM)
        self.main_sizer.Add(temp,1,wx.EXPAND)
        self.main_sizer.Fit(self.main_window)



        self.active_node=None
        """
        This attribute contains the node that is currently displayed onscreen
        """


        self.is_playing=False
        """
        Says whether the simulation is currently playing.
        """

        self.delay=0.05 # Should be a mechanism for setting that
        self.default_buffer=50 # Should be a mechanism for setting that

        self.timer_for_playing=None
        """
        Contains the wx.Timer object used when playing the simulation
        """

        self.paths=[]
        """
        Contains a list of paths.
        todo: is there really a need for this?
        """

        self.path=None
        """
        The active path.
        """

        self.ran_out_of_tree_while_playing=False
        """
        Becomes True when you are playing the simulation and the nodes
        are not ready yet. The simulation will continue playing
        when the nodes will be created.
        """

        main_window.Bind(wx.EVT_MENU,self.edit_from_active_node,id=s2i("Fork by editing"))
        main_window.Bind(wx.EVT_MENU,self.step_from_active_node,id=s2i("Fork naturally"))

        self.simulation_package=simulation_package
        simulation_package.initialize(self)
        wx.CallAfter(self.make_initial_dialog)

    def make_initial_dialog(self):
        if hasattr(self.simulation_package,"make_initial_dialog"):
            return self.simulation_package.make_initial_dialog(self)
        else:
            return self.make_generic_initial_dialog()

    def show_state(self,state):
        self.simulation_package.show_state(self,state)

    def set_parent_window(self,parent_window):
        self.main_window.Reparent(parent_window)

    def set_active_path(self,path):
        """
        Sets `path` as the active path,
        also adding it to self.paths if necessary.
        """
        if not path in self.paths:
            self.paths.append(path)
        self.path=path

    def make_plain_root(self,*args,**kwargs):
        """
        Creates a parent-less node, whose state is a simple plain state.
        The SimulationCore subclass should define the function "make_plain_state"
        for this to work.
        Updates the active path to start from this root.
        Starts crunching on this new root.
        Returns the node.
        """
        root=self.project.make_plain_root(*args,**kwargs)
        if self.path==None:
            self.path=garlicsim.state.Path(self.project.tree,root)
        else:
            self.path.start=root
        self.project.crunch_all_edges(root,self.default_buffer)
        self.make_active_node(root)
        return root

    def make_random_root(self,*args,**kwargs):
        """
        Creates a parent-less node, whose state is a random and messy state.
        The SimulationCore subclass should define the function "make_random_state"
        for this to work.
        Updates the active path to start from this root.
        Starts crunching on this new root.
        Returns the node.
        """
        root=self.project.make_random_root(*args,**kwargs)
        if self.path==None:
            self.path=garlicsim.state.Path(self.project.tree,root)
        else:
            self.path.start=root
        self.project.crunch_all_edges(root,self.default_buffer)
        self.make_active_node(root)
        return root

    def make_active_node_and_correct_path(self,node):
        """
        Makes "node" the active node, displaying it onscreen.
        Also modifies the active path so that it will go through
        that node.
        """
        if node in self.path:
            self.make_active_node(node)
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
        self.make_active_node(node)

    def make_active_node(self,node):
        """
        Makes "node" the active node, displaying it onscreen.
        """
        self.project.crunch_all_edges(node,self.default_buffer)
        was_playing=False
        if self.is_playing==True:
            self.stop_playing()
            was_playing=True
        self.show_state(node.state)
        self.active_node=node
        if was_playing==True:
            self.start_playing()
        self.main_window.Refresh()


    def start_playing(self):
        """
        Starts playback of the simulation.
        """
        if self.is_playing==True:
            return
        if self.active_node==None:
            return

        self.is_playing=True
        self.timer_for_playing=wx.FutureCall(self.delay*1000,functools.partial(self.__play_next,self.active_node))


    def stop_playing(self):
        """
        Stops playback of the simulation.
        """
        if self.is_playing==False:
            return
        self.is_playing=False
        try:
            self.timer_for_playing.Stop()
        except:
            pass
        self.project.crunch_all_edges(self.active_node,self.default_buffer)



    def __editing_state(self):
        node=self.active_node
        state=node.state
        if state.is_touched()==False or node.still_in_editing==False:
            new_node=self.edit_from_active_node()
            return new_node.state
        else:
            return state

    def toggle_playing(self):
        """
        If the simulation is currently playing, stops it.
        Otherwise, starts playing.
        """
        if self.is_playing:
            return self.stop_playing()
        else:
            return self.start_playing()


    def __play_next(self,node):
        """
        A function called repeatedly while playing the simualtion.
        """
        self.show_state(node.state)
        self.main_window.Refresh()
        self.active_node=node
        try:
            next_node=self.path.next_node(node)
        except IndexError:
            self.ran_out_of_tree_while_playing=True
            return
        self.timer_for_playing=wx.FutureCall(self.delay*1000,functools.partial(self.__play_next,next_node))

    def step_from_active_node(self,*args,**kwargs):
        """
        Used for forking the simulation without
        modifying any states.
        Creates a new node from the active node via
        natural simulation.
        Returns the new node.

        todo: maybe not let to do it from unfinalized touched node?
        """
        new_node=self.project.step(self.active_node)
        self.make_active_node(new_node)
        self.notify_paths_of_fork(new_node.parent,new_node)
        return new_node

    def edit_from_active_node(self,*args,**kwargs):
        """
        Used for forking the simulation by editing.
        Creates a new node from the active node via
        editing.
        Returns the new node.
        """
        new_node=self.project.tree.new_touched_state(template_node=self.active_node)
        new_node.still_in_editing=True
        self.make_active_node(new_node)
        self.notify_paths_of_fork(self.active_node.parent,new_node)
        return new_node



    def notify_paths_of_fork(self,parent_node,child_node):
        """
        Notifies all the paths in self.paths of the new fork.
        Why should the paths be notified? Because they need to
        know which fork of the road to choose.
        """

        if parent_node==None:
            self.path.start=child_node
            return

        non_active_paths=[path for path in self.paths if path!=self.path]

        if self.path!=None:
            self.path.decisions[parent_node]=child_node
        for path in non_active_paths:
            if path.decisions.has_key(parent_node)==False:
                path.decisions[parent_node]=parent_node.children[0]

    def sync_workers(self):
        """
        A wrapper for Project.sync_workers(). (todo: add real explanation)
        Returns how many nodes were added to the tree.
        """

        if self.is_playing:
            playing_edge=self.path.get_last(starting_at=self.active_node)
        else:
            playing_edge=None


        added_nodes=self.project.sync_workers(temp_infinity_node=playing_edge)
        """
        This is the important line here, which actually executes
        the Project's sync_workers function. As you can see,
        we put the return value in `added_nodes`.
        """

        if added_nodes>0:
            self.main_window.Refresh()
        if self.ran_out_of_tree_while_playing==True:
            self.ran_out_of_tree_while_playing=False
            self.stop_playing()
            self.start_playing()
        return added_nodes



    def get_node_menu(self):
        nodemenu=wx.Menu()
        nodemenu.Append(s2i("Fork by editing"),"Fork by &editing"," Create a new edited node with the current node as the template")
        nodemenu.Append(s2i("Fork naturally"),"Fork &naturally"," Run the simulation from this node")
        nodemenu.AppendSeparator()
        nodemenu.Append(s2i("Delete..."),"&Delete..."," Delete the node")
        return nodemenu

    def done_editing(self):
        node=self.active_node
        if node.still_in_editing==False:
            raise StandardError("You said 'done editing', but you were not in editing mode.")
        node.still_in_editing=False
        self.project.crunch_all_edges(node, self.default_buffer)

    def make_generic_initial_dialog(self):
        initial_dialog=customwidgets.GenericInitialDialog(self.main_window, -1)
        if initial_dialog.ShowModal()==wx.ID_OK:
            if initial_dialog.info["random"]:
                self.make_random_root()
            else:
                self.make_plain_root()
        initial_dialog.Destroy()


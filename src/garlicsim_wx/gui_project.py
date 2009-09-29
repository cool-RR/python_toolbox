# Copyright 2009 Ram Rachum.
# This program is not licensed for distribution and may not be distributed.

import wx
import wx.lib.scrolledpanel as scrolled

import functools
try: import queue
except ImportError: import Queue as queue

import garlicsim.misc.queue_tools as queue_tools
from misc.stringsaver import s2i,i2s
from garlicsim.misc.infinity import Infinity
import garlicsim
import warnings

import copy

import custom_widgets
FoldableWindowContainer=custom_widgets.FoldableWindowContainer

import wx.py.shell


class GuiProject(object):
    """
    A GuiProject encapsulates a Project for use with a wxPython
    interface.
    """
    def __init__(self, simpack, parent_window):
        self.__init_general(simpack, parent_window)
        self.__init_on_creation()
        
    def __init_general(self, simpack, parent_window, project=None,
                       active_node=None, path=None):
    
        self.simpack = garlicsim.misc.module_wrapper.ModuleWrapper(simpack)
        
        if project:
            self.project = project
        else:
            self.project = garlicsim.Project(simpack)

        main_window = self.main_window = \
                    wx.ScrolledWindow(parent_window,-1)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_window.SetSizer(self.main_sizer)

        self.state_showing_window = \
            scrolled.ScrolledPanel(self.main_window, -1)

        locals_for_shell = locals()
        locals_for_shell.update({"this_gui_project": self})
        self.shell = wx.py.shell.Shell(self.main_window, -1,
                                       size=(400, -1), locals=locals_for_shell)
        self.seek_bar = custom_widgets.SeekBar(self.main_window, -1, self)
        self.tree_browser = custom_widgets.TreeBrowser(self.main_window,
                                                       -1, self)


        self.top_fwc = FoldableWindowContainer(self.main_window, -1,
                                               self.state_showing_window,
                                               self.shell, wx.RIGHT,
                                               folded=True)
        temp = FoldableWindowContainer(self.main_window, -1, self.top_fwc,
                                       self.seek_bar, wx.BOTTOM)
        temp = FoldableWindowContainer(self.main_window, -1, temp,
                                       self.tree_browser, wx.BOTTOM)
        self.main_sizer.Add(temp, 1, wx.EXPAND)
        self.main_sizer.Fit(self.main_window)

        self.active_node = active_node
        """
        This attribute contains the node that is currently displayed onscreen
        """

        self.is_playing = False
        """
        Says whether the simulation is currently playing.
        """

        self.delay = 0.05 # Should be a mechanism for setting that
        self.default_buffer = 50 # Should be a mechanism for setting that

        self.timer_for_playing=None
        """
        Contains the wx.Timer object used when playing the simulation
        """

        self.path = path
        """
        The active path.
        """

        self.ran_out_of_tree_while_playing = False
        """
        Becomes True when you are playing the simulation and the nodes
        are not ready yet. The simulation will continue playing
        when the nodes will be created.
        """

        main_window.Bind(wx.EVT_MENU,self.edit_from_active_node,id=s2i("Fork by editing"))
        main_window.Bind(wx.EVT_MENU,self.fork_naturally,id=s2i("Fork naturally"))
     
        
        simpack.initialize(self)
                
        self.stuff_to_do_when_idle = queue.Queue()
        self.main_window.Bind(wx.EVT_IDLE, self.on_idle)

    def __init_on_creation(self):
        wx.CallAfter(self.make_initial_dialog)
    
    def make_initial_dialog(self):
        if hasattr(self.simpack,"make_initial_dialog"):
            return self.simpack.make_initial_dialog(self)
        else:
            return self.make_generic_initial_dialog()

    def show_state(self,state):
        self.simpack.show_state(self,state)

    def set_parent_window(self,parent_window):
        self.main_window.Reparent(parent_window)
        
    def on_idle(self, event=None):
        try:
            mission = self.stuff_to_do_when_idle.get(block=False)
            mission()
            event.RequestMore(True)
        except queue.Empty:
            pass
                

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
        self.set_active_node(root)
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
        self.set_active_node(root)
        return root

    def set_active_node(self, node, modify_path=True):
        """
        Makes "node" the active node, displaying it onscreen.
        """
        self.project.crunch_all_leaves(node, self.default_buffer)
        
        was_playing = self.is_playing
        if self.is_playing: self.stop_playing()

        self.show_state(node.state)
        self.active_node = node
        if was_playing:
            self.start_playing()
        if modify_path:
            self.__modify_path_to_include_active_node()
        self.main_window.Refresh()

    def __modify_path_to_include_active_node(self):
        """
        Makes sure that self.path goes through the active node,
        replacing it with another path if it doesn't.
        """
        if self.path is None:
            self.path = self.active_node.make_containing_path()
            return
        if not self.active_node in self.path:
            self.path.modify_to_include_node(self.active_node)


    def start_playing(self):
        """
        Starts playback of the simulation.
        """
        if self.is_playing is True:
            return
        if self.active_node is None:
            return

        self.is_playing = True
        
        def mission():
            self.timer_for_playing = wx.FutureCall(self.delay*1000, functools.partial(self.__play_next, self.active_node))
        self.stuff_to_do_when_idle.put(mission)


    def stop_playing(self):
        """
        Stops playback of the simulation.
        """
        if self.timer_for_playing is not None:
            try:
                self.timer_for_playing.Stop()
            except:
                pass
        if self.is_playing is False:
            return
        self.is_playing = False
        queue_tools.dump_queue(self.stuff_to_do_when_idle)
        assert self.stuff_to_do_when_idle.qsize() == 0
        self.project.crunch_all_leaves(self.active_node, self.default_buffer)



    def __editing_state(self):
        node=self.active_node
        state=node.state
        if node.touched is False or node.still_in_editing is False:
            new_node=self.edit_from_active_node()
            return new_node.state
        else:
            return state

    def toggle_playing(self):
        """
        If the simulation is currently playing, stops it.
        Otherwise, starts playing.
        """
        return self.stop_playing() if self.is_playing else self.start_playing()


    def __play_next(self, node):
        """
        A function called repeatedly while playing the simulation.
        """
        if self.is_playing is False: return
        self.show_state(node.state)
        self.main_window.Refresh() # Make more efficient?
        self.active_node = node
        try:
            next_node = self.path.next_node(node)
        except garlicsim.data_structures.path.PathOutOfRangeError:
            self.ran_out_of_tree_while_playing = True
            return
        
        def mission():
            self.timer_for_playing = wx.FutureCall(self.delay*1000,
                                                   functools.partial(self.__play_next,
                                                                     next_node))
            
        self.stuff_to_do_when_idle.put(mission)
        

    def fork_naturally(self, *args, **kwargs):
        """
        Used for forking the simulation without modifying any states.
        Creates a new node from the active node via natural simulation.

        todo: maybe not let to do it from unfinalized touched node?
        """
        
        node = self.active_node
        if self.project.nodes_to_crunch.has_key(node):
            return # Problem: Node is already a leaf. Todo.
        else:
            self.project.nodes_to_crunch[node] = self.default_buffer

    def edit_from_active_node(self,*args,**kwargs):
        """
        Used for forking the simulation by editing.
        Creates a new node from the active node via
        editing.
        Returns the new node.
        """
        new_node = self.project.tree.fork_by_editing(template_node=self.active_node)
        new_node.still_in_editing = True
        self.set_active_node(new_node)
        return new_node


    def sync_crunchers(self):
        """
        A wrapper for Project.sync_crunchers(). (todo: add real explanation)
        Returns how many nodes were added to the tree.
        """

        if self.is_playing:
            playing_leaf = self.path.get_last_node(starting_at=self.active_node)
        else:
            playing_leaf = None


        added_nodes=self.project.sync_crunchers(temp_infinity_node=playing_leaf)
        """
        This is the important line here, which actually executes
        the Project's sync_crunchers function. As you can see,
        we put the return value in `added_nodes`.
        """

        if added_nodes>0:
            self.tree_modify_refresh()
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
        self.project.crunch_all_leaves(node, self.default_buffer)

    def make_generic_initial_dialog(self):
        initial_dialog=custom_widgets.GenericInitialDialog(self.main_window, -1)
        if initial_dialog.ShowModal()==wx.ID_OK:
            if initial_dialog.info["random"]:
                self.make_random_root()
            else:
                self.make_plain_root()
        initial_dialog.Destroy()

    def tree_modify_refresh(self):
        self.seek_bar.Refresh()
        self.tree_browser.Refresh()
        
    def tickle(self):
        stuff_we_want = ["project", "path", "active_node", "simpack"]
        my_dict = {}
        for thing in stuff_we_want:
            my_dict[thing] = self.__dict__[thing]
        return my_dict
    
def load_tickled_gui_project(tickled_gui_project, parent_window):
    gui_project = GuiProject.__new__(GuiProject)
    
    simpack = tickled_gui_project.pop("simpack")
    
    gui_project._GuiProject__init_general(simpack, parent_window,
                                          **tickled_gui_project)
    return gui_project
        
    
    
    
# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `StepProfilesList` class.

See its documentation for more details.
'''

import wx
import weakref

from garlicsim_wx.general_misc import wx_tools
from garlicsim_wx.widgets.general_misc import cute_hyper_tree_list

import garlicsim, garlicsim_wx
from garlicsim_wx.widgets import WorkspaceWidget

from .free_context_menu import FreeContextMenu
from .step_profile_context_menu import StepProfileContextMenu
from .step_profile_item_panel import StepProfileItemPanel


class StepProfilesList(cute_hyper_tree_list.CuteHyperTreeList):
    '''
    List of step profiles.
    
    The list has all the step profiles that are used in the tree, and also the
    step profiles that the user created but aren't in the tree yet.
    
    The `StepProfilesList` allows the user to add new step profiles (possibly
    by using existing ones as templates, or by starting from scratch,) to
    delete existing step profiles, and to change the hue used to identify the
    step profile in the GUI.
    
    '''
    # todo: set max size dynamically according to number of profiles
    
    def __init__(self, step_profiles_controls, frame):
        
        self.frame = frame
        assert isinstance(self.frame, garlicsim_wx.Frame)
        self.gui_project = frame.gui_project
        assert isinstance(self.gui_project, garlicsim_wx.GuiProject)
        self.step_profiles_controls = step_profiles_controls
        
        cute_hyper_tree_list.CuteHyperTreeList.__init__(
            self,
            step_profiles_controls,
            style=wx.SIMPLE_BORDER,
            agwStyle=(
                #wx.TR_FULL_ROW_HIGHLIGHT | \
                wx.TR_ROW_LINES | \
                wx.TR_HIDE_ROOT | \
                cute_hyper_tree_list.TR_NO_HEADER
                )
        )        
        
        self.step_profiles_to_items = weakref.WeakKeyDictionary()
        
        self.AddColumn('', width=50)
        self.AddColumn('', width=600)
        self.SetMainColumn(1)
        self.root_item = self.AddRoot('')
        
        self.items = self.root_item._children
        
        self.free_context_menu = FreeContextMenu(self)
        self.step_profile_context_menu = StepProfileContextMenu(self)
        
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self._on_tree_item_activated)
        
        self.Bind(wx.EVT_TREE_ITEM_MENU, self._on_tree_item_menu)
        self.Bind(wx.EVT_CONTEXT_MENU, self._on_context_menu)
        
        self.Bind(wx.EVT_TREE_BEGIN_DRAG, self._on_tree_begin_drag)
        
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self._on_tree_sel_changed)
        
        self.GetMainWindow().Bind(wx.EVT_KEY_DOWN, self._on_key_down)
        
        self.gui_project.step_profiles_set_modified_emitter.add_output(
            self.update
        )
        
        self.gui_project.active_step_profile_changed_emitter.add_output(
            self.update_active_step_profile_indicator
        )
        
        self.update_active_step_profile_indicator()
        
  
        
    def update(self):
        '''Ensure we're showing exactly the gui project's step profiles.'''
        
        gui_project = self.gui_project
        
        for step_profile, item in self.step_profiles_to_items.items():
            if item not in self.items:
                del self.step_profiles_to_items[step_profile]
                
        for step_profile in gui_project.step_profiles:
            try:
                item = self.step_profiles_to_items[step_profile]
            except KeyError:
                step_profile_item_panel = StepProfileItemPanel(self,
                                                               step_profile)
                item = self.AppendItem(self.root_item, '',
                                       )#wnd=step_profile_item_panel)
                item.SetWindow(step_profile_item_panel, 0)
                item.step_profile = step_profile
                item.step_profile_item_panel = step_profile_item_panel
                self.step_profiles_to_items[step_profile] = item
                self.SetItemText(
                    item,
                    step_profile.__repr__(short_form=True,
                                          root=gui_project.simpack,
                                          namespace=gui_project.namespace),
                    1
                )
        
        for item in self.items:
            if item.step_profile not in gui_project.step_profiles:
                self.Delete(item)
                # item.step_profile_item_panel.Destroy()
                # Apparently gets destroyed before

        
        if (self.items) and (self.GetSelection() not in self.items):
            self.SelectItem(self.items[-1])
            
            
                
               
    def update_active_step_profile_indicator(self):
        '''
        Ensure we're putting the active step profile marker on the active one.
        '''
        active_step_profile = self.gui_project.get_active_step_profile()
        for item in self.items:
            active_step_profile_indicator = \
                item.step_profile_item_panel.active_step_profile_indicator
            step_profile = item.step_profile
            if step_profile == active_step_profile:
                active_step_profile_indicator.set_active()
            else:
                active_step_profile_indicator.set_inactive()
        
    
    def get_selected_step_profile(self):
        '''Get the step profile that's currently selected.'''
        selection = self.GetSelection()
        if selection and (selection != self.root_item):
            return selection.step_profile
        else:
            return None
        
        
    def select_step_profile(self, step_profile):
        '''Select `step_profile`.'''
        item = self.step_profiles_to_items[step_profile]
        self.SelectItem(item)
        
        
    def _on_tree_item_activated(self, event):
        assert event.GetItem() == self.GetSelection()
        self.step_profiles_controls.show_step_profile_editing_dialog(
            self.get_selected_step_profile()
        )
    
    
    def _on_tree_item_menu(self, event):
        abs_position = event.GetPoint() or wx.DefaultPosition
        
        if abs_position == wx.DefaultPosition:
            position = (0, 0) # todo: take position smartly
        else:
            position = self.ScreenToClient(abs_position)

        if self.get_selected_step_profile() is not None:
            self.PopupMenu(self.step_profile_context_menu, position)
        else:
            new_event = wx.ContextMenuEvent(
                wx.wxEVT_CONTEXT_MENU,
                self.GetId(),
                abs_position #self.ClientToScreen(abs_position)
            )
            new_event.SetEventObject(self)
            wx.PostEvent(self, new_event)
            
    
            
    def _on_context_menu(self, event):

        abs_position = event.GetPosition()
        
        if abs_position == wx.DefaultPosition:
            position = (0, 0)
        else:
            position = self.ScreenToClient(abs_position)
            
        self.PopupMenu(self.free_context_menu, position)
        
        
    def _on_new_step_profile_button(self, event):
        self.step_profiles_controls.show_step_profile_editing_dialog()

        
    def _on_fork_by_crunching_button(self, event):
        self.gui_project.fork_by_crunching(
            self.get_selected_step_profile()
        )

        
    def _on_select_tree_members_button(self, event):
        raise NotImplementedError()

        
    def _on_change_color_button(self, event):
        item = self.GetSelection()
        item.step_profile_item_panel.hue_control.open_editing_dialog()

        
    def _on_duplicate_and_edit_button(self, event):
        self.step_profiles_controls.show_step_profile_editing_dialog(
            self.get_selected_step_profile()
        )

        
    def _on_tree_begin_drag(self, event):
        event.Allow()
        
        
    def _on_tree_end_drag(self, event):
        event.Allow()
        
    
    def _on_tree_sel_changed(self, event):
        event.Skip()
        self.step_profiles_controls._recalculate()
       
        
    def _on_key_down(self, event):
        key = wx_tools.keyboard.Key.get_from_key_event(event)
        if key == wx_tools.keyboard.Key(wx.WXK_DELETE):
            self.step_profiles_controls.try_delete_step_profile(
                self.get_selected_step_profile()
            )
        else:
            event.Skip()
            
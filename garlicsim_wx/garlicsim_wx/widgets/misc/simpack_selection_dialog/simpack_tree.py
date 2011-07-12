# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `SimpackTree` class.

See its documentation for more info.
'''

import os
import sys
import glob
import pkgutil
import itertools
import collections

import wx
import pkg_resources

from garlicsim.general_misc.comparison_tools import underscore_hating_key
from garlicsim.general_misc import address_tools
from garlicsim.general_misc import path_tools
from garlicsim.general_misc import dict_tools
from garlicsim.general_misc import cute_iter_tools
from garlicsim.general_misc import sequence_tools
from garlicsim.general_misc import import_tools
from garlicsim.general_misc import package_finder
from garlicsim.general_misc.nifty_collections import OrderedDict
from garlicsim_wx.general_misc import wx_tools
from garlicsim_wx.widgets.general_misc.cute_tree_ctrl import CuteTreeCtrl

import garlicsim
import garlicsim_wx
import garlicsim_lib
from garlicsim.misc import simpack_tools
from garlicsim.misc.simpack_tools import SimpackMetadata
from garlicsim_wx.misc.simpack_place import SimpackPlace

from . import images as __images_package
images_package = __images_package.__name__


class SimpackTree(CuteTreeCtrl):
    '''
    Widget showing a simpack tree, from which we can select a simpack.
    
    The tree can be filtered using the navigation panel's search box.
    '''
    
    def __init__(self, simpack_selection_dialog):
        CuteTreeCtrl.__init__(
            self,
            parent=simpack_selection_dialog,
            style=wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT | wx.SUNKEN_BORDER
        )
        
        assert isinstance(simpack_selection_dialog, SimpackSelectionDialog)
        self.simpack_selection_dialog = simpack_selection_dialog
        
        self.SetHelpText('Here you can see the different simpacks available. '
                         'Choose one of them in order to start a project. If '
                         'you want to use simpacks from a different location, '
                         'press the "Add simpacks from a different folder..." '
                         'button below.')
        
        self.__init_images()
        
        self._simpack_places_tree = OrderedDict()
        self._filtered_simpack_places_tree = OrderedDict()
        self._simpack_places_to_items = {}
        self._simpack_places_to_expansion_states = {}
        
        
        #self.AddColumn('', width=600)
        #self.SetMainColumn(1)
        self.root_item = self.AddRoot('All simpack places')
        
        self.bind_event_handlers(SimpackTree)
        

    def __init_images(self):
        self._simpack_bitmap = wx_tools.bitmap_tools.bitmap_from_pkg_resources(
            images_package,
            'simpack.png'
        )
        self._closed_folder_bitmap = \
            wx_tools.generic_bitmaps.get_closed_folder_bitmap()
        self._open_folder_bitmap = \
            wx_tools.generic_bitmaps.get_open_folder_bitmap()
        
        self._bitmaps = [
            self._simpack_bitmap,
            self._closed_folder_bitmap,
            self._open_folder_bitmap
        ]
        
        (self._SIMPACK_BITMAP_INDEX,
         self._CLOSED_FOLDER_BITMAP_INDEX,
         self._OPEN_FOLDER_BITMAP_INDEX) = range(3)
        
        self._image_list = wx.ImageList(16, 16, initialCount=0)
        for bitmap in self._bitmaps:
            self._image_list.Add(bitmap)
            
        self.SetImageList(self._image_list)

    
    def _reload_internal_trees(self):
        
        # Ensuring all simpack place paths are in `sys.path`:
        for simpack_place in garlicsim_wx.simpack_places:
            if simpack_place.path not in sys.path:
                sys.path.append(simpack_place.path)
            
        filter_words = self.simpack_selection_dialog.navigation_panel.\
                                                        filter_box.filter_words
        
        new_simpack_places_tree = OrderedDict()
        new_filtered_simpack_places_tree = OrderedDict()
            
        for simpack_place in garlicsim_wx.simpack_places:
            
            simpacks = simpack_place.get_simpack_metadatas()
            simpacks.sort(key=lambda simpack_metadata: simpack_metadata.name)
            new_simpack_places_tree[simpack_place] = simpacks
            
            
            filtered_simpacks = \
                [simpack_metadata for simpack_metadata in simpacks if
                 simpack_metadata.matches_filter_words(filter_words,
                                                       simpack_place)]
            
            if filtered_simpacks or not filter_words or \
                              simpack_place.matches_filter_words(filter_words):
                new_filtered_simpack_places_tree[simpack_place] = \
                                                              filtered_simpacks
            
        self._simpack_places_tree = new_simpack_places_tree
        self._filtered_simpack_places_tree = new_filtered_simpack_places_tree
            
            
    def reload_tree(self):        
        
        self._reload_internal_trees()
        
        #######################################################################
        #######################################################################
        ### Updating simpack places: ##########################################
        #                                                                     #
        
        ### Removing deleted simpack places: ##################################
        #                                                                     #
        simpack_place_items = self.get_children_of_item(self.root_item)
        for simpack_place_item in simpack_place_items:
            simpack_place = self.GetItemPyData(simpack_place_item)
            if simpack_place not in self._filtered_simpack_places_tree:
                self._simpack_places_to_expansion_states[simpack_place] = \
                    self.IsExpanded(simpack_place_item)
                self.Delete(simpack_place_item)
        #                                                                     #
        ### Finished removing deleted simpack places. #########################
            
        ### Adding new simpack places: ########################################
        #                                                                     #
        simpack_place_items = self.get_children_of_item(self.root_item)
        simpack_places_that_have_items = \
            [self.GetItemPyData(simpack_place_item) for simpack_place_item
            in simpack_place_items]
        simpack_place_items = self.get_children_of_item(self.root_item)
        for simpack_place in self._filtered_simpack_places_tree:
            if simpack_place not in simpack_places_that_have_items:
                # blocktodo: can extract this block into method:
                new_simpack_place_item = self.AppendItem(
                    self.root_item,
                    text=simpack_place.name
                )
                self.SetItemPyData(new_simpack_place_item,
                                   simpack_place)
                self.SetItemImage(new_simpack_place_item,
                                  self._CLOSED_FOLDER_BITMAP_INDEX,
                                  which=wx.TreeItemIcon_Normal)
                self.SetItemImage(new_simpack_place_item,
                                  self._OPEN_FOLDER_BITMAP_INDEX,
                                  which=wx.TreeItemIcon_Expanded)
                self._simpack_places_to_items[simpack_place] = \
                                                         new_simpack_place_item
                
        self.SortChildren(self.root_item)
        #                                                                     #
        ### Finished adding new simpack places. ###############################
        
        simpack_place_items = self.get_children_of_item(self.root_item)
        assert len(simpack_place_items) == \
                                        len(self._filtered_simpack_places_tree)
        
        #                                                                     #
        ### Finished updating simpack places. #################################
        #######################################################################
        #######################################################################
        
        #######################################################################
        #######################################################################
        ### Updating simpacks: ################################################
        #                                                                     #

        for simpack_place in self._filtered_simpack_places_tree:

            simpack_place_item = self._simpack_places_to_items[simpack_place]
            
            simpack_metadatas = \
                              self._filtered_simpack_places_tree[simpack_place]
            
            simpack_items = self.get_children_of_item(simpack_place_item)
            simpack_metadatas_that_have_items = \
                [self.GetItemPyData(simpack_item) for simpack_item
                 in simpack_items]
            
            ### Removing deleted simpacks: ####################################
            #                                                                 #
            for simpack_item in simpack_items:
                simpack_metadata = self.GetItemPyData(simpack_item)
                if simpack_metadata not in simpack_metadatas:
                    self.Delete(simpack_item)
            #                                                                 #
            ### Finished removing deleted simpacks. ###########################
                    
            ### Adding new simpacks: ##########################################
            #                                                                 #
            for simpack_metadata in simpack_metadatas:
                if simpack_metadata not in simpack_metadatas_that_have_items:
                    new_simpack_item = self.AppendItem(
                        simpack_place_item,
                        text=simpack_metadata.name
                    )
                    self.SetItemPyData(new_simpack_item,
                                       simpack_metadata)
                    self.SetItemImage(new_simpack_item,
                                      self._SIMPACK_BITMAP_INDEX,
                                      which=wx.TreeItemIcon_Normal)
            #                                                                 #
            ### Finished adding new simpacks. #################################
            
            self.SortChildren(simpack_place_item)
            
            simpack_items = self.get_children_of_item(simpack_place_item)
            assert len(simpack_items) == len(simpack_metadatas)
        
        #                                                                     #
        ### Finished updating simpacks. #######################################
        #######################################################################
        #######################################################################
        
        # (Doing expansion/collapsion of simpack place items only now, because
        # we can't expand a folder before it had items in it.)
        for simpack_place, expansion_state in \
                              self._simpack_places_to_expansion_states.items():
            if simpack_place in self._filtered_simpack_places_tree:
                del self._simpack_places_to_expansion_states[simpack_place]
                simpack_place_item = \
                                   self._simpack_places_to_items[simpack_place]
                if expansion_state is True:
                    self.Expand(simpack_place_item)
                else: # expansion_state is False
                    self.Collapse(simpack_place_item)

                    
    def refresh_tree_and_ensure_simpack_selected(self):
        self.reload_tree()
        self.ensure_simpack_selected()
        
        
    def ensure_simpack_selected(self):
        
        if not self._filtered_simpack_places_tree or not \
                              any(self._filtered_simpack_places_tree.values()):
            # If there are no simpacks, do nothing.
            return
        
        # If the flow reached here, we know that we have at least one simpack
        # in the tree. We're gonna try and select a reasonable one.

        # Let's see what kind of item is currently selected:
        selected_item = self.GetSelection()
        
        if not selected_item.Ok() or \
                       self.GetItemText(selected_item) == 'All simpack places':
            # Either nothing is selected or the invisible root item is
            # selected. Select the first simpack:
            self._select_first_simpack()
            
        elif type(self.GetItemPyData(selected_item)) is SimpackPlace:
            # A simpack place is selected.
             
            
            # If it contains simpacks, select the first one:...
            possible_simpack_item, _ = self.GetFirstChild(selected_item)
            if possible_simpack_item.Ok():
                self.SelectItem(possible_simpack_item)
            else:
                # ...Otherwise select the first simpack in the tree:
                self._select_first_simpack()
        else:
            assert type(self.GetItemPyData(selected_item)) is SimpackMetadata
            # A simpack is already selected, we don't need to do anything.

            
    def _select_first_simpack(self):
        simpack_item = self._get_simpack_items()[0]
        self.SelectItem(simpack_item)
                                
        
    def _get_simpack_items(self):
        return self.get_children_of_item(self.root_item, generations=2)
    
    
    def refresh(self):
        new_simpack_metadata = self.simpack_selection_dialog.simpack_metadata
        if (new_simpack_metadata is not None) and (self.GetItemPyData(self.
            GetSelection()) is not new_simpack_metadata):
            assert new_simpack_metadata is not None
            filter_box = \
                      self.simpack_selection_dialog.navigation_panel.filter_box
            
            simpack_item = self._get_simpack_item_deleting_filter_words(
                new_simpack_metadata,
                filter_box
            )
                            
            self.SelectItem(simpack_item)

    def _get_simpack_item_deleting_filter_words(self,
                                                new_simpack_metadata,
                                                filter_box):
        try:
            simpack_item = self._get_simpack_item_of_simpack_metadata(
                new_simpack_metadata
            )
        except LookupError:
            while filter_box.filter_words:
                try: 
                    simpack_item = \
                        self._get_simpack_item_of_simpack_metadata(
                            new_simpack_metadata
                        )
                except LookupError:
                    new_filter_words = filter_box.filter_words[:-1]
                    filter_box.Value = ' '.join(new_filter_words)
                    self.simpack_selection_dialog.refresh()
                else:
                    break
            else:
                try:
                    simpack_item = \
                        self._get_simpack_item_of_simpack_metadata(
                            new_simpack_metadata
                        )
                except LookupError:
                    raise LookupError("Deleted all filter words, but still "
                                      "can't find the requested simpack "
                                      "metadata. Perhaps the simpack was "
                                      "deleted.")
        return simpack_item

            
    def _get_simpack_item_of_simpack_metadata(self, new_simpack_metadata):
        simpack_items = self._get_simpack_items()
        matching_simpack_items = \
            [simpack_item for simpack_item in simpack_items if
             self.GetItemPyData(simpack_item) is new_simpack_metadata]
        assert len(matching_simpack_items) in (0, 1)
        if matching_simpack_items:
            (matching_simpack_item,) = matching_simpack_items
            return matching_simpack_item
        else:
            raise LookupError("The given `simpack_metadata` has no "
                              "corresponding item in the tree; possibly it's "
                              "been filtered out using the filter box.")
            
            
    def OnComapreItems(self, item_1, item_2):
        item_1_data = self.GetItemPyData(item_1)
        item_2_data = self.GetItemPyData(item_)
        assert type(item_1_data) == type(item_2_data)
        data_type = type(item_1_data)
        if data_type is SimpackPlace:
            return cmp(item_1_data.path, item_2_data.path)
        else:
            assert data_type is SimpackMetadata
            return cmp(item_1_data.name, item_2_data.name) or \
                   cmp(item_1_data.address, item_2_data.address)
        
        
    def _on_tree_sel_changed(self, event):
        data = self.GetItemPyData(self.GetSelection())
        if type(data) is SimpackMetadata:
            self.simpack_selection_dialog.set_simpack_metadata(data)
        else:
            self.simpack_selection_dialog.set_simpack_metadata(None)
            
            
    def _on_tree_item_activated(self, event):
        item = event.GetItem()
        data = self.GetItemPyData(item)
        if isinstance(data, SimpackMetadata):
            simpack_metadata = data
            self.simpack_selection_dialog.\
                                         set_simpack_metadata(simpack_metadata)
            self.simpack_selection_dialog.simpack = simpack_metadata.\
                                                               import_simpack()
            self.simpack_selection_dialog.EndModal(wx.ID_OK)
        
            
    def _on_char(self, event):
        # Doesn't work on Mac and Linux; probably the generic tree control
        # swallows keystrokes.
        key = wx_tools.keyboard.Key.get_from_key_event(event)
        if key.is_alphanumeric():            
            filter_box = self.simpack_selection_dialog.navigation_panel.\
                                                                     filter_box
            filter_box.SetFocus()
            current_filter_string = filter_box.Value
            add_space = not current_filter_string.endswith(u' ')
            new_filter_string = current_filter_string + (u' ' * add_space) + \
                                                                   unicode(key)
            filter_box.Value = new_filter_string
            filter_box.SetSelection(len(filter_box.Value),
                                    len(filter_box.Value))
            
        else:
            event.Skip()
            
        
from .simpack_selection_dialog import SimpackSelectionDialog
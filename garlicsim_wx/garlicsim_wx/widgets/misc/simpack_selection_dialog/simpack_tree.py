# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `SimpackTree` class.

See its documentation for more info.
'''

import sys

import wx

from garlicsim.general_misc.nifty_collections import OrderedDict
from garlicsim_wx.general_misc import wx_tools
from garlicsim_wx.widgets.general_misc.cute_tree_ctrl import CuteTreeCtrl

import garlicsim_wx
from garlicsim.misc.simpack_tools import SimpackMetadata
from garlicsim_wx.misc.simpack_place import SimpackPlace

from . import images as __images_package
images_package = __images_package.__name__


class SimpackTree(CuteTreeCtrl):
    '''
    Widget showing a simpack tree, from which we can select a simpack.
    
    The folders in the tree are simpack places (i.e. folder in which the user
    wants to search simpacks) and their child-items are simpacks.
        
    The tree can be filtered using the navigation panel's search box.
    
    When a simpack is selected in the tree, information about it is shown in
    the `SimpackInfoPanel`, and if we double-click it on the tree (or press
    Enter) a new project will be started with that simpack.
    '''
    
    def __init__(self, simpack_selection_dialog):
        CuteTreeCtrl.__init__(
            self,
            parent=simpack_selection_dialog,
            style=wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT | wx.SUNKEN_BORDER
        )
        
        assert isinstance(simpack_selection_dialog, SimpackSelectionDialog)
        self.simpack_selection_dialog = simpack_selection_dialog
        
        self.HelpText = ('Here you can see the different simpacks available. '
                         'Choose one of them in order to start a project. If '
                         'you want to use simpacks from a different location, '
                         'press the "Add simpacks from a different folder..." '
                         'button below.')
        
        self.__init_images()
        
        self._simpack_places_tree = OrderedDict()
        '''
        A tree containing all the simpack places and simpacks.
        
        This is an ordered dict from each simpack place to a list of
        simpack-metadatas of the simpacks that reside in it.
        
        This is not a filtered tree; it contains *all* the simpack places and
        simpacks and it's not being filtered or otherwise affected by the
        `FilterBox`.
        '''
        
        self._filtered_simpack_places_tree = OrderedDict()
        '''
        A tree containing the simpack places and simpacks after filtering.
        
        This is an ordered dict from each simpack place to a list of
        simpack-metadatas of the simpacks that reside in it.
        
        Only those simpacks and simpack places that were accepted by the filter
        words in `FilterBox` will be admitted into this tree.
        '''
        
        self._simpack_places_to_items = {}
        '''A dict from each simpack place to its item in the visual tree.'''
        
        self._simpack_places_to_expansion_states = {}
        '''
        A dict from each simpack place to the last expansion state of its item.
        
        "Expansion state" is merely a `bool` that records whether the simpack
        place's item was expanded in the tree or not. This is stored only for
        simpack place items that have been removed from the visual tree, so
        next time we'll show them we'll put them in the same expansion state
        they were last in. At this point we will also remove them from this
        dict.
        '''
        
        self.root_item = self.AddRoot('All simpack places')
        '''
        The root item that all simpack place items will be children of.
        
        This is never shown visually on the screen, but we still maintain it
        because `wx.TreeCtrl` always needs to have exactly one root item.
        '''
        
        self.bind_event_handlers(SimpackTree)
        

    def __init_images(self):
        '''Create bitmaps/images to be used as icons for tree items.'''
        
        self._simpack_bitmap = wx_tools.bitmap_tools.bitmap_from_pkg_resources(
            images_package,
            'simpack.png'
        )
        '''Bitmap of a simpack, showing a crate with the GarlicSim logo.'''
        
        self._closed_folder_bitmap = \
            wx_tools.generic_bitmaps.get_closed_folder_bitmap()
        '''Bitmap of a closed folder.'''
        
        self._open_folder_bitmap = \
            wx_tools.generic_bitmaps.get_open_folder_bitmap()
        '''Bitmap of an open folder.'''
        
        self._bitmaps = [
            self._simpack_bitmap,
            self._closed_folder_bitmap,
            self._open_folder_bitmap
        ]
        '''List of all item bitmaps.'''
        
        (self._SIMPACK_BITMAP_INDEX,
         self._CLOSED_FOLDER_BITMAP_INDEX,
         self._OPEN_FOLDER_BITMAP_INDEX) = range(3)
        '''Indices of the different bitmaps in the bitmap list.'''
        
        self._image_list = wx.ImageList(16, 16, initialCount=0)
        for bitmap in self._bitmaps:
            self._image_list.Add(bitmap)
            
        self.SetImageList(self._image_list)

        
    ###########################################################################
    ###########################################################################
    ### Methods for refreshing and reloading: #################################
    #                                                                         #
    
    def _reload_internal_trees(self):
        '''
        Recalculate the two internal trees of simpack places and simpacks.
        
        These are `._simpack_places_tree` and `._filtered_simpack_places_tree`.
        
        This function ensures that the currently-active simpack places are in
        the tree, and that for each of them all the simpacks are listed.
        '''
        # Ensuring all simpack place paths are in `sys.path`:
        for simpack_place in garlicsim_wx.simpack_places:
            if simpack_place.path not in sys.path:
                sys.path.append(simpack_place.path)
            
        filter_words = self.simpack_selection_dialog.navigation_panel.\
                                                        filter_box.filter_words
        
        new_simpack_places_tree = OrderedDict()
        new_filtered_simpack_places_tree = OrderedDict()
            
        for simpack_place in garlicsim_wx.simpack_places:
            
            ### Putting simpacks in `._simpack_places_tree`: ##################
            #                                                                 #
            simpacks = simpack_place.get_simpack_metadatas()
            simpacks.sort(key=lambda simpack_metadata: simpack_metadata.name)
            new_simpack_places_tree[simpack_place] = simpacks
            #                                                                 #
            ### Finished putting simpacks in `._simpack_places_tree`. #########
            
            ### Putting simpacks in `.filtered_simpack_places_tree`: ##########
            #                                                                 #
            filtered_simpacks = \
                [simpack_metadata for simpack_metadata in simpacks if
                 simpack_metadata.matches_filter_words(filter_words,
                                                       simpack_place)]
            
            if filtered_simpacks or not filter_words or \
                              simpack_place.matches_filter_words(filter_words):
                new_filtered_simpack_places_tree[simpack_place] = \
                                                              filtered_simpacks
            #                                                                 #
            ### Finished putting simpacks in `.filtered_simpack_places_tree`. #
            
        self._simpack_places_tree = new_simpack_places_tree
        self._filtered_simpack_places_tree = new_filtered_simpack_places_tree
            
            
    def reload_tree(self, ensure_simpack_selected=False):
        '''
        Reload the visual tree on the screen.
        
        The internal trees are first updated, and then the visual tree gets
        updated to match the filtered internal tree.
        '''
        self._reload_internal_trees()
        
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
        for simpack_place in self._filtered_simpack_places_tree:
            if simpack_place not in simpack_places_that_have_items:
                self._create_simpack_place_item(simpack_place)
                
        self.SortChildren(self.root_item) # Sorting simpack places by path
        #                                                                     #
        ### Finished adding new simpack places. ###############################
        
        simpack_place_items = self.get_children_of_item(self.root_item)
        assert len(simpack_place_items) == \
                                        len(self._filtered_simpack_places_tree)
        
        #                                                                     #
        ### Finished updating simpack places. #################################
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
            simpack_items_to_delete = \
                [simpack_item for simpack_item in simpack_items if
                 self.GetItemPyData(simpack_item) not in simpack_metadatas]
            
            for simpack_item in simpack_items_to_delete:
                self.Delete(simpack_item)
            #                                                                 #
            ### Finished removing deleted simpacks. ###########################
                    
            ### Adding new simpacks: ##########################################
            #                                                                 #
            for simpack_metadata in simpack_metadatas:
                if simpack_metadata not in simpack_metadatas_that_have_items:
                    self._create_simpack_item(simpack_place_item,
                                              simpack_metadata)
            #                                                                 #
            ### Finished adding new simpacks. #################################
            
            self.SortChildren(simpack_place_item) # Sorting simpacks by name
            
            simpack_items = self.get_children_of_item(simpack_place_item)
            assert len(simpack_items) == len(simpack_metadatas)
        
        #                                                                     #
        ### Finished updating simpacks. #######################################
        #######################################################################
        
        ### Expanding/collapsing simpack place items: #########################
        #                                                                     #
        
        # We need to expand/collapse simpack place items that were previously
        # removed from the tree and now re-added. We are returning them to the
        # same expansion state they had before being removed.
        #
        # (The reason that we're doing this at the end of the method is because
        # we can't expand a folder before it has any items in it.)
        
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
        #                                                                     #
        ### Finished expanding/collapsing simpack place items. ################

        if ensure_simpack_selected:
            self.ensure_simpack_selected()

            
    def refresh(self):
        '''Refresh the tree, making it show the selected simpack-metadata.'''
        new_simpack_metadata = self.simpack_selection_dialog.simpack_metadata
        
        selected_item = self.GetSelection()
        if (new_simpack_metadata is not None) and \
           ((not selected_item.IsOk()) or
           (self.GetItemPyData(selected_item) is not new_simpack_metadata)):
            
            self._select_simpack_item_deleting_filter_words(
                new_simpack_metadata,
            )
            
    #                                                                         #
    ### Finished methods for refreshing and reloading. ########################
    ###########################################################################
    ###########################################################################
    
    ###########################################################################
    ###########################################################################
    ### Methods for creating new items: #######################################
    #                                                                         #
    
    def _create_simpack_item(self, simpack_place_item, simpack_metadata):
        '''
        Create simpack item for `simpack_metadata` under `simpack_place_item`.
        '''
        new_simpack_item = self.AppendItem(
            simpack_place_item,
            text=simpack_metadata.name
        )
        self.SetItemPyData(new_simpack_item,
                           simpack_metadata)
        self.SetItemImage(new_simpack_item,
                          self._SIMPACK_BITMAP_INDEX,
                          which=wx.TreeItemIcon_Normal)

            
    def _create_simpack_place_item(self, simpack_place):
        '''Create simpack place item for `simpack_place`.'''
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

    #                                                                         #
    ### Finished methods for creating new items. ##############################
    ###########################################################################
    ###########################################################################
        
    ###########################################################################
    ###########################################################################
    ### Methods for selecting items: ##########################################
    #                                                                         #
        
    def ensure_simpack_selected(self):
        '''
        Ensure that a simpack is selected.
        
        If a simpack is not currently selected, we'll try to select a simpack
        belonging to the currently-selected simpack place, if one is selected;
        otherwise, we'll just select the first simpack in the tree.
        '''
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
        '''Select the first simpack item in the visual tree.'''
        simpack_item = self._get_simpack_items()[0]
        self.SelectItem(simpack_item)
    
            
    def _select_simpack_item_deleting_filter_words(self, simpack_metadata):
        '''
        Select item of `simpack_metadata` deleting filter words as needed.
        
        This is a tricky method: It's being given a `simpack_metadata`, and its
        goal is to set the simpack item that corresponds to it as selected.
        But, that simpack item might not currently exist because there may be
        filter words in the `FilterBox` that are causing it to be filtered out.
        If this is the case, this method will delete the filter words one by
        one until the simpack will no longer be filtered out and it will have a
        simpack item in the visual tree. Then it will be selected.
        '''
        
        filter_box = self.simpack_selection_dialog.navigation_panel.filter_box
        try:
            # First let's try to get the simpack item naively:
            return self.SelectItem(
                self._get_simpack_item_of_simpack_metadata(
                    simpack_metadata
                )
            )
        
        except LookupError:
            # If the flow reached here, the simpack item does not exist in the
            # tree! Let's remove filter words one-by-one (and reload the tree
            # each time) until the simpack item appears.
            while filter_box.filter_words:
                try: 
                    return self.SelectItem(
                        self._get_simpack_item_of_simpack_metadata(
                            simpack_metadata
                        )
                    )
                except LookupError:
                    # Remove the last filter word:
                    new_filter_words = filter_box.filter_words[:-1]
                    filter_box.Value = ' '.join(new_filter_words)
                    self.simpack_selection_dialog.refresh()
            else:
                # All the filter words have been removed; now we'll make a
                # final attempt at getting the simpack item and selecting it:
                try:
                    return self.SelectItem(
                        self._get_simpack_item_of_simpack_metadata(
                            simpack_metadata
                        )
                    )
                except LookupError:
                    raise LookupError("Deleted all filter words, but still "
                                      "can't find the requested simpack "
                                      "metadata. Perhaps the simpack was "
                                      "deleted.")

    #                                                                         #
    ### Finished methods for selecting items. #################################
    ###########################################################################
    ###########################################################################

    ###########################################################################
    ###########################################################################
    ### Methods for retrieving items: #########################################
    #                                                                         #
        
    def _get_simpack_items(self):
        '''Get all the simpack items in the visual tree.'''
        return self.get_children_of_item(self.root_item, generations=2)
    
    
    def _get_simpack_item_of_simpack_metadata(self, simpack_metadata):
        '''Get the simpack item of `simpack_metadata`.'''
        simpack_items = self._get_simpack_items()
        matching_simpack_items = \
            [simpack_item for simpack_item in simpack_items if
             self.GetItemPyData(simpack_item) is simpack_metadata]

        # There must either exactly one match, or none:
        assert len(matching_simpack_items) in (0, 1)
        
        if matching_simpack_items:
            (matching_simpack_item,) = matching_simpack_items
            return matching_simpack_item
        else:
            raise LookupError("The given `simpack_metadata` has no "
                              "corresponding item in the tree; possibly it's "
                              "been filtered out using the filter box.")
    
    #                                                                         #
    ### Finished methods for retrieving items. ################################
    ###########################################################################
    ###########################################################################
            
    
    def _compare_items(self, item_1, item_2):
        '''
        Compare `item_1` to `item_2`.
        
        Returns `1` if `item_1 > item_2`, returns `-1` if `item_1 < item_2`,
        and `0` if they are equal.
        
        This is a hook used by `CuteTreeCtrl`.
        
        If the compared items are simpack items, they are sorted by name, with
        the address being a tiebreaker. If the compared items are simpack place
        items, they are compared by path.
        '''
        item_1_data = self.GetItemPyData(item_1)
        item_2_data = self.GetItemPyData(item_2)
        assert type(item_1_data) == type(item_2_data)
        data_type = type(item_1_data)
        if data_type is SimpackPlace:
            return cmp(item_1_data.path, item_2_data.path)
        else:
            assert data_type is SimpackMetadata
            return cmp(item_1_data.name, item_2_data.name) or \
                   cmp(item_1_data.address, item_2_data.address)
    
    
    ###########################################################################
    ###########################################################################
    ### Event handlers: #######################################################
    #                                                                         #
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
    #                                                                         #
    ### Finished event handlers. ##############################################
    ###########################################################################
    ###########################################################################
            
        
from .simpack_selection_dialog import SimpackSelectionDialog
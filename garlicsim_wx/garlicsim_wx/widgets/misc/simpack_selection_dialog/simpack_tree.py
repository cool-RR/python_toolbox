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
import collections

import wx
import pkg_resources

from garlicsim.general_misc.comparison_tools import underscore_hating_key
from garlicsim.general_misc import address_tools
from garlicsim.general_misc import path_tools
from garlicsim.general_misc import dict_tools
from garlicsim.general_misc import import_tools
from garlicsim.general_misc import package_finder
from garlicsim.general_misc.nifty_collections import OrderedDict
from garlicsim_wx.general_misc import wx_tools
from garlicsim_wx.widgets.general_misc.cute_tree_ctrl import CuteTreeCtrl

import garlicsim_wx
import garlicsim_lib
from garlicsim.misc import simpack_tools
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
        self._simpack_places_to_items = {}
        self._simpack_places_to_expansion_states = {}
        
        
        #self.AddColumn('', width=600)
        #self.SetMainColumn(1)
        self.root_item = self.AddRoot('All simpack places')
        

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

    
    def _refresh_internal_tree(self):
        
        # Ensuring all simpack place paths are in `sys.path`:
        for simpack_place in garlicsim_wx.simpack_places:
            if simpack_place.path not in sys.path:
                sys.path.append(simpack_place.path)
            
        filter_words = self.simpack_selection_dialog.navigation_panel.\
                                                        filter_box.filter_words
        
        new_simpack_places_tree = OrderedDict()
            
        for simpack_place in garlicsim_wx.simpack_places:
            
            path, package_prefix, name = simpack_place
            
            ### Determining path to search: ###################################
            #                                                                 #
            if package_prefix:
                assert package_prefix[-1] == '.'
                package = address_tools.resolve(package_prefix[:-1])
                path_to_search = path_tools.get_path_of_package(package)
            else: # not package_prefix
                path_to_search = path
            #                                                                 #
            ### Finished determining path to search. ##########################
                
            simpack_addresses = [
                (package_prefix + package_name[1:]) for package_name in
                package_finder.get_packages(path_to_search, self_in_name=False)
            ]
            
            simpacks = []
            
            for simpack_address in simpack_addresses:
                simpack_metadata = simpack_tools.SimpackMetadata.\
                                   create_from_address(simpack_address)
                if simpack_metadata.matches_filter_words(filter_words):
                    simpacks.append(simpack_metadata)
            
            simpacks.sort(key=lambda simpack_metadata: simpack_metadata.name)
            
            if simpacks:
                new_simpack_places_tree[simpack_place] = simpacks
            
        self._simpack_places_tree = new_simpack_places_tree
            
            
    def refresh_tree(self):        
        
        self._refresh_internal_tree()
        
        #######################################################################
        #######################################################################
        ### Updating simpack places: ##########################################
        #                                                                     #
        
        ### Removing deleted simpack places: ##################################
        #                                                                     #
        simpack_place_items = self.get_children_of_item(self.root_item)
        for simpack_place_item in simpack_place_items:
            simpack_place = self.GetItemPyData(simpack_place_item)
            if simpack_place not in self._simpack_places_tree:
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
        for simpack_place in self._simpack_places_tree:
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
        #                                                                     #
        ### Finished adding new simpack places. ###############################
        
        simpack_place_items = self.get_children_of_item(self.root_item)
        assert len(simpack_place_items) == len(self._simpack_places_tree)
        
        #                                                                     #
        ### Finished updating simpack places. #################################
        #######################################################################
        #######################################################################
        
        #######################################################################
        #######################################################################
        ### Updating simpacks: ################################################
        #                                                                     #

        for simpack_place in self._simpack_places_tree:

            simpack_place_item = self._simpack_places_to_items[simpack_place]
            
            simpack_metadatas = self._simpack_places_tree[simpack_place]
            
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
            
            
            simpack_items = self.get_children_of_item(simpack_place_item)
            assert len(simpack_items) == len(simpack_metadatas)
        
        #                                                                     #
        ### Finished updating simpacks. #######################################
        #######################################################################
        #######################################################################
        
        # (Doing expansion/collapsion of simpack place items only now, because
        # we can't expand a folder before it had items in it.)
        for simpack_place, expansion_state in \
             dict_tools.devour_items(self._simpack_places_to_expansion_states):
            simpack_place_item = self._simpack_places_to_items[simpack_place]
            if expansion_state is True:
                self.Expand(simpack_place_item)
            else: # expansion_state is False
                self.Collapse(simpack_place_item)

        
from .simpack_selection_dialog import SimpackSelectionDialog
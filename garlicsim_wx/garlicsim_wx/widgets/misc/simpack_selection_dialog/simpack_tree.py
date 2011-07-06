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

import wx
import pkg_resources

from garlicsim.general_misc.comparison_tools import underscore_hating_key
from garlicsim.general_misc import address_tools
from garlicsim.general_misc import path_tools
from garlicsim.general_misc import import_tools
from garlicsim.general_misc import package_finder
from garlicsim.general_misc.nifty_collections import OrderedDict
from garlicsim_wx.general_misc import wx_tools
from garlicsim_wx.widgets.general_misc.cute_tree_ctrl import CuteTreeCtrl

import garlicsim_wx
import garlicsim_lib
from garlicsim.misc import simpack_tools

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
        
        self.simpack_places_tree = []
        
        
        
        
        #self.AddColumn('', width=600)
        #self.SetMainColumn(1)
        self.root_item = self.AddRoot('All simpack places')
        # blocktodo: make uncollapsable if possible
        
        self.SetItemImage(self.root_item,
                          self._CLOSED_FOLDER_BITMAP_INDEX,
                          which=wx.TreeItemIcon_Normal)
        self.SetItemImage(self.root_item,
                          self._OPEN_FOLDER_BITMAP_INDEX,
                          which=wx.TreeItemIcon_Expanded)
        
        #titles = ["Conway's Game of Life", "Prisoner's Dilemma",
                  #'Queueing Theory']
        #for title in titles:
            #item = self.AppendItem(self.root_item_id, title)
            #self.SetItemImage(item,
                              #self._SIMPACK_BITMAP_INDEX,
                              #wx.TreeItemIcon_Normal)
        
        self.ExpandAll()
        self.refresh_tree()

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
        for path, package_prefix in garlicsim_wx.simpack_places:
            if path not in sys.path:
                sys.path.append(path)
            
        
        del self.simpack_places_tree[:]
            
        for path, package_prefix in garlicsim_wx.simpack_places:
            
            ### Determining name for simpack place: ###########################
            #                                                                 #
            name = None
            
            if package_prefix:
                parent_package = address_tools.resolve(package_prefix[:-1])
                if hasattr(parent_package, 'simpack_place_name'):
                    name = getattr(parent_package, 'simpack_place_name')
                    
            if name is None:
                name = os.path.split(path)[-1]
            #                                                                 #
            ### Finished determining name for simpack place. ##################
            
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
                
                simpacks.append(simpack_metadata)
            
            simpacks.sort(key=lambda simpack_metadata: simpack_metadata.name)
            
            entry = {'name': name,
                     'path': path,
                     'simpacks': simpacks,
                     'item': None}
            
            self.simpack_places_tree.append(entry)
            
            
    def refresh_tree(self):        
        
        self._refresh_internal_tree()
        
        #######################################################################
        #######################################################################
        ### Updating simpack places: ##########################################
        #                                                                     #
        
        ### Removing deleted simpack places: ##################################
        #                                                                     #
        existing_simpack_place_paths = [entry['path'] for entry in
                                        self.simpack_places_tree]
        simpack_place_items = self.get_children_of_item(self.root_item)
        for simpack_place_item in simpack_place_items:
            if self.GetItemPyData(simpack_place_item) not in \
                                                  existing_simpack_place_paths:
                self.Delete(simpack_place_item)
        #                                                                     #
        ### Finished removing deleted simpack places. #########################
            
        ### Adding new simpack places: ########################################
        #                                                                     #
        paths_of_simpack_place_items = [self.GetItemPyData(simpack_place_item)
                                        for simpack_place_item in
                                        simpack_place_items]
        simpack_place_items = self.get_children_of_item(self.root_item)
        for simpack_place in self.simpack_places_tree:
            if simpack_place['path'] not in paths_of_simpack_place_items:
                # blocktodo: can extract this block into method:
                new_item = self.AppendItem(self.root_item,
                                           text=simpack_place['name'])
                self.SetItemPyData(new_item, simpack_place['path'])
                self.SetItemImage(new_item,
                                  self._CLOSED_FOLDER_BITMAP_INDEX,
                                  which=wx.TreeItemIcon_Normal)
                self.SetItemImage(new_item,
                                  self._OPEN_FOLDER_BITMAP_INDEX,
                                  which=wx.TreeItemIcon_Expanded)
                simpack_place['item'] = new_item
        #                                                                     #
        ### Finished adding new simpack places. ###############################
        
        simpack_place_items = self.get_children_of_item(self.root_item)
        assert len(simpack_place_items) == len(self.simpack_places_tree)
        
        #                                                                     #
        ### Finished updating simpack places. #################################
        #######################################################################
        #######################################################################
        
        #######################################################################
        #######################################################################
        ### Updating simpacks: ################################################
        #                                                                     #

        for simpack_place in self.simpack_places_tree:
            
            pass#for simpack_metadata in simpack_place['simpacks']:
                
        
        #                                                                     #
        ### Finished updating simpacks. #######################################
        #######################################################################
        #######################################################################

        
from .simpack_selection_dialog import SimpackSelectionDialog
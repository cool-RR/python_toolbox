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
from garlicsim_wx.widgets.general_misc import cute_hyper_tree_list

import garlicsim_wx
import garlicsim_lib
from garlicsim.misc import simpack_tools

from . import images as __images_package
images_package = __images_package.__name__


class SimpackTree(wx.TreeCtrl):
    '''
    Widget showing a simpack tree, from which we can select a simpack.
    
    The tree can be filtered using the navigation panel's search box.
    '''
    
    def __init__(self, simpack_selection_dialog):
        wx.TreeCtrl.__init__(
            self,
            parent=simpack_selection_dialog,
            style=wx.TR_DEFAULT_STYLE | wx.SUNKEN_BORDER
        )
        
        assert isinstance(simpack_selection_dialog, SimpackSelectionDialog)
        self.simpack_selection_dialog = simpack_selection_dialog
        
        self.__init_images()
        
        self.simpack_places_tree = []
        
        
        
        
        #self.AddColumn('', width=600)
        #self.SetMainColumn(1)
        self.root_item_id = self.AddRoot("GarlicSim's simpack library")
        self.SetItemImage(self.root_item_id,
                          self._CLOSED_FOLDER_BITMAP_INDEX,
                          which=wx.TreeItemIcon_Normal)
        self.SetItemImage(self.root_item_id,
                          self._OPEN_FOLDER_BITMAP_INDEX,
                          which=wx.TreeItemIcon_Expanded)
        
        titles = ["Conway's Game of Life", "Prisoner's Dilemma",
                  'Queueing Theory']
        for title in titles:
            item = self.AppendItem(self.root_item_id, title)
            self.SetItemImage(item,
                              self._SIMPACK_BITMAP_INDEX,
                              wx.TreeItemIcon_Normal)
        
        self.ExpandAll()

    def __init_images(self):
        self._simpack_bitmap = wx.BitmapFromImage(
            wx.ImageFromStream(
                pkg_resources.resource_stream(images_package,
                                              'simpack.png'),
                wx.BITMAP_TYPE_ANY
            )
        )
        self._closed_folder_bitmap = wx_tools.get_closed_folder_bitmap()
        self._open_folder_bitmap = wx_tools.get_open_folder_bitmap()
        
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
            
            simpacks.sort(key=lambda simpack_metadata: simpack_metadata)
            
            entry = {'name': name,
                     'path': path,
                     'simpacks': simpacks}
            
            self.simpack_places_tree.append(entry)
            
            
    def refresh_simpacks(self):        
        
        
        self.RootItem
            
        #for roots in self.GetRootItem

        
from .simpack_selection_dialog import SimpackSelectionDialog
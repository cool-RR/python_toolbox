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

from garlicsim.general_misc.cmp_tools import underscore_hating_key
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
    
    def __init__(self, simpack_selection_dialog):
        wx.TreeCtrl.__init__(
            self,
            parent=simpack_selection_dialog,
            style=wx.TR_DEFAULT_STYLE | wx.SUNKEN_BORDER
        )
        
        assert isinstance(simpack_selection_dialog, SimpackSelectionDialog)
        self.simpack_selection_dialog = simpack_selection_dialog
        
        #self.AddColumn('', width=600)
        #self.SetMainColumn(1)
        self.root_item_id = self.AddRoot("GarlicSim's simpack library")
        self.AppendItem(self.root_item_id, "Conway's Game of Life")
        self.AppendItem(self.root_item_id, "Prisoner's Dilemma")
        self.AppendItem(self.root_item_id, 'Queueing Theory')

        
    def refresh_simpacks(self):        

        # Ensuring all simpack place paths are in `sys.path`:
        for path, package_prefix in garlicsim_wx.simpack_places:
            if path not in sys.path:
                sys.path.append(path)
            
        
        simpack_places_tree = []
            
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
                     'simpacks': []}
            
            simpack_places_tree.append(entry)
            

        
from .simpack_selection_dialog import SimpackSelectionDialog
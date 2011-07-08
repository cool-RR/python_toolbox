# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
A wxPython-based GUI for garlicsim.

The final goal of this project is to become a fully-fledged application for
working with simulations, friendly enough that it may be used by
non-programmers.

This program is intended for Python versions 2.5, 2.6 and 2.7, using wxPython
version 2.8.10.1 and upwards. (But not including 2.9.x, which is a development
release.)
'''

from . import bootstrap

import sys
import os.path

import wx

from garlicsim.general_misc import path_tools

import garlicsim.general_misc.version_info

import garlicsim
import garlicsim_wx
import garlicsim_lib

from . import misc
from .frame import Frame
from .gui_project import GuiProject
from .app import App


__all__ = ['Frame', 'GuiProject', 'start']


__version_info__ = garlicsim.general_misc.version_info.VersionInfo(0, 6, 3)
__version__ = '0.6.3'

simpack_places = []
'''
Places were simpacks may be found, described as `(path, package_prefix)` pairs.

The `path` part says the path that simpacks should be imported with; i.e., the
path that should be in `sys.path` for the simpack to be importable.

The `package_prefix` part, which may be an empty string, is the hierarchy of
packages up to the simpacks. For example, a simpack place may have a package
prefix of `'garlicsim_lib.simpacks.'`, in which case `garlicsim_wx` will try to
import any simpacks that are in the `garlicsim_lib.simpacks` package. If an
empty string is given, the path itself will be used without going into any
packages inside of it.
'''


def start():
    '''Start the GUI.'''
    
    from garlicsim_wx.misc.simpack_place import SimpackPlace
    
    # The first argument is the path of the script (or the executable if we're
    # frozen), and that should be cut off:    
    args = sys.argv[1:]
    
    # todo: Consider removing the args we can understand from sys.argv, so
    # program inside will not be confused by them.
        
    new_gui_project_simpack_name = None
    load_gui_project_file_path = None
    
    ### Adding simpack places that we were given: #############################
    #                                                                         #
    garlicsim_wx.simpack_places = [
        SimpackPlace(
            path_tools.get_root_path_of_module(garlicsim_lib),
            'garlicsim_lib.simpacks.'
        ),
    ]
    
    for arg in args:
        if arg.startswith('__garlicsim_wx_simpack_place='):
            simpack_place = SimpackPlace(*(arg[29:].split(',')))
            if simpack_place not in garlicsim_wx.simpack_places:
                garlicsim_wx.simpack_places.append(simpack_place)
    
    for simpack_place in garlicsim_wx.simpack_places:
        if simpack_place.path not in sys.path:
            sys.path.append(simpack_place.path)
    #                                                                         #
    ### Finished adding simpack places that we were given. ####################
            
    if args:
        arg = args[0]        
        if arg.startswith('__garlicsim_wx_new='):
            new_gui_project_simpack_name = arg[19:]
        elif os.path.isfile(arg):
            load_gui_project_file_path = arg
            
    import random
    random.seed()
    
    app = App(new_gui_project_simpack_name=new_gui_project_simpack_name,
              load_gui_project_file_path=load_gui_project_file_path)
    
    app.MainLoop()
    
    
if __name__ == "__main__":
    
    start()
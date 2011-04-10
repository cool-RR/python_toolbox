# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `PlayerType` metaclass.

See its documentation for more information.
'''

from __future__ import absolute_import

import random
from garlicsim.general_misc.third_party import abc

from garlicsim.general_misc import caching


class PlayerType(abc.ABCMeta):
    '''Metaclass for player types.'''
        
    @caching.CachedProperty
    def wx_color(cls):
        '''The wxPython color that represents this player type in the GUI.'''
        import wx
        return wx.NamedColour(cls.color or 'Red')
    
    
    @staticmethod
    def create_player_of_random_type():
        '''Create a player of a random player type.'''
        from .players import player_types_list
        player_type = random.choice(player_types_list)
        return player_type()
        
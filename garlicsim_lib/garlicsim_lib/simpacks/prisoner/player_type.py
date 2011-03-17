# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `PlayerType` class.

See its documentation for more information.
'''

from __future__ import absolute_import

import random
from garlicsim.general_misc.third_party import abc

from garlicsim.general_misc import caching


class PlayerType(abc.ABCMeta):
    ''' '''
    
    @caching.CachedProperty
    def wx_color(self):
        import wx
        return wx.NamedColour(self.color or 'Red')
    
    @staticmethod
    def create_random_strategy_player():
        from .players import player_types_list
        player_type = random.choice(player_types_list)
        return player_type()
        

    
    
# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `BasePlayer` class.

See its documentation for more information.
'''

from garlicsim.general_misc.third_party import abc

from .player_type import PlayerType


class BasePlayer(object):
    __metaclass__ = PlayerType

    color = None
    
    
    def __init__(self):
        self.points = 0

        
    @abc.abstractmethod
    def play(self, round):
        ''''''

    
    def other_player_played(self, move):
        pass
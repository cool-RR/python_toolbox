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
        ''' '''
    
    def other_player_played(self, move):
        pass
    
    
    def play_game(player_1, player_2, round):
        
        assert isinstance(player_1, BasePlayer)
        assert isinstance(player_2, BasePlayer)
    
        player_1_move = player_1.play(round)
        player_2_move = player_2.play(round)
    
        assert isinstance(player_1_move, bool)
        assert isinstance(player_2_move, bool)
    
        if player_1_move is True and player_2_move is True:
            player_1.points += 1
            player_2.points += 1
            
        elif player_1_move is True and player_2_move is False:
            player_1.points += -4
            player_2.points += 2
            
        elif player_1_move is False and player_2_move is True:
            player_1.points += 2
            player_2.points += -4
            
        elif player_1_move is False and player_2_move is False:
            player_1.points += -1
            player_2.points += -1
    
        player_1.other_player_played(player_2_move)
        player_2.other_player_played(player_1_move)
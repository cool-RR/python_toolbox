# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Simpack for a repeating game of prisoner's dillema with natural selection.
'''

import random

from garlicsim.general_misc import random_tools
import garlicsim.data_structures

from .player_type import PlayerType
from .base_player import BasePlayer
from .players import player_types_list


class State(garlicsim.data_structures.State):
    
    def __init__(self, players, round=-1, match=0, n_rounds=7):
        self.round = round
        self.match = match
        self.players = players
        self.n_rounds = n_rounds
        
    
    @staticmethod
    def create_root(n_players=70, n_rounds=7):
        state = State(
            players=[player_types_list[i % len(player_types_list)]() for i
                     in xrange(n_players)],
            n_rounds=n_rounds
        )
        state._prepare_for_new_match(replace_loser=False)
        return state
    
    
    @staticmethod
    def create_messy_root(n_players=70, n_rounds=7):
        state = State(
            players=[PlayerType.create_random_strategy_player() for i
                     in xrange(n_players)],
            n_rounds=n_rounds
        )
        state._prepare_for_new_match(replace_loser=False)
        return state
    
        
    def inplace_step(self):
        self.clock += 1
    
        self.round += 1
        if self.round == self.n_rounds:
            self.round = -1
            self.match += 1
            self._prepare_for_new_match()
            return
    
        for player_1, player_2 in self.player_pairs:
            BasePlayer.play_game(player_1, player_2, self.round)
    
    
    def _prepare_for_new_match(self, replace_loser=True):
        '''
        Note: this function is not strictly a "step function":
        it manipulates the state that is given to it and then returns it.
        '''
        assert self.round == -1
        
        if replace_loser:
            loser = self.get_player_with_least_points()
            self.players.remove(loser)
            self.players.append(PlayerType.create_random_strategy_player())
    
        self.player_pairs = random_tools.random_partition(self.players, 2)
        
        
    def get_player_with_least_points(self):
        return min(self.players, key=lambda player: player.points)

    
    def get_n_players_of_given_type(self, player_type):
        return len([player for player in self.players
                    if isinstance(player, player_type)])




    


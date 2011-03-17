# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Simpack for a repeating game of prisoner's dillema with natural selection.
'''

import random
random.seed()

from garlicsim.general_misc import random_tools
import garlicsim.data_structures

from .player import BasePlayer
from .players import player_types_list


class State(garlicsim.data_structures.State):
    
    def __init__(self, round, match, players, n_rounds=7):
        self.round = round
        self.match = match
        self.players = players
        self.n_rounds = n_rounds
        
    
    @staticmethod
    def create_root(n_players=70, n_rounds=7):
        state = State(
            round=-1,
            match=0,
            players=[
                player_types[i % len(player_types_list)]() for \
                i in xrange(n_players)
            ],
            n_rounds=n_rounds
        )
        state._prepare_for_new_match()
        return state
    
    
    @staticmethod
    def create_messy_root(n_players=70, n_rounds=7):
        global player_types
        state = State(
            round=-1,
            match=0,
            players=[BasePlayer.create_random_strategy_player() for i
                     in xrange(n_players)],
            n_rounds=n_rounds
        )
        state._prepare_for_new_match()
        return state
    
        
    def inplace_step(self):
        self.clock += 1
    
        self.round += 1
        if self.round == self.n_rounds:
            self.round = -1
            self.match += 1
            self._prepare_for_new_match()
            return
    
        for pair in self.pairs:
            play_game(pair, self.round)
    
    
    def _prepare_for_new_match(self):
        '''
        Note: this function is not strictly a "step function":
        it manipulates the state that is given to it and then returns it.
        '''
        loser = self.get_player_with_least_points()
        self.players.remove(loser)
        self.players.append(BasePlayer.create_random_strategy_player())
    
        self.pairs = random_tools.random_partition(self.players, 2)
        
        
    def get_player_with_least_points(self):
        return min(self.players, key=lambda player: player.points)

    
    def get_n_players_of_given_type(self, player_type):
        return len([player for player in self.players
                    if isinstance(player, player_type)])


def play_game((x, y), round):
    x_move = x.play(round)
    y_move = y.play(round)

    assert isinstance(x_move, bool)
    assert isinstance(y_move, bool)

    if x_move is True and y_move is True:
        x.points += 1
        y.points += 1
    elif x_move is True and y_move is False:
        x.points += -4
        y.points += 2
    elif x_move is False and y_move is True:
        x.points += 2
        y.points += -4
    elif x_move is False and y_move is False:
        x.points += -1
        y.points += -1

    x.other_player_played(y_move)
    y.other_player_played(x_move)

    








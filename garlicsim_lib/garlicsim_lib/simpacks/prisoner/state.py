# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `State` class.

See its documentation for more information.
'''


import random

from garlicsim.general_misc import random_tools
from garlicsim.general_misc.infinity import infinity


import garlicsim.data_structures

from .player_type import PlayerType
from .base_player import BasePlayer
from .players import player_types_list


class State(garlicsim.data_structures.State):
    '''World state. A frozen moment in time in the simulation world.'''
    
    def __init__(self, players, round=-1, match=0, n_rounds=7):
        '''
        Constructor.
        
        `players` is a list of players, i.e. instances of `BasePlayer`, that
        will play against each other. `round` is the round number, with `-1`
        being the preparation pseudo-round. `match` is the match number.
        `n_rounds` is the number of rounds in a match.
        '''
        
        assert -1 <= round <= (n_rounds - 1)
        self.round = round
        '''
        The round number.
        
        `-1` is the preparation pseudo-round, `0` is the first round, and
        `n_rounds - 1` is the last round in the match .
        '''
        
        assert 0 <= match <= infinity
        self.match = match
        '''The match number, going from `0` to infinity.'''
        
        assert all(isinstance(player, BasePlayer) for player in players)
        self.players = players
        '''The list of players that play against each other.'''
        
        assert n_rounds >= 1
        self.n_rounds = n_rounds
        '''The number of rounds in a match.'''
        
    
    @staticmethod
    def create_root(n_players=70, n_rounds=7):
        '''Create a plain and featureless world state.'''
        state = State(
            players=[player_types_list[i % len(player_types_list)]() for i
                     in xrange(n_players)],
            n_rounds=n_rounds
        )
        state._prepare_for_new_match(replace_loser=False)
        return state
    
    
    @staticmethod
    def create_messy_root(n_players=70, n_rounds=7):
        '''Create a random and messy world state.'''
        state = State(
            players=[PlayerType.create_player_of_random_type() for i
                     in xrange(n_players)],
            n_rounds=n_rounds
        )
        state._prepare_for_new_match(replace_loser=False)
        return state
    
        
    def inplace_step(self):
        '''Modify the state in-place to make it the next moment in time.'''
        
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
        Prepare a state with a `.round` of `-1` for the new match.
        
        Round -1 is a pseudo round in which the players get partitioned into
        pairs randomly. The two players in each player will play against each
        other in every round in the match, after which they'll be reassigned a
        new opponent.
        
        If `replace_loser` is set to `True`, the player with the least points
        will be removed and replaced with a player from a random player type.
        '''
        assert self.round == -1
        
        if replace_loser:
            loser = self.get_player_with_least_points()
            self.players.remove(loser)
            self.players.append(PlayerType.create_player_of_random_type())
    
        self.player_pairs = random_tools.random_partitions(
            self.players,
            2,
            allow_remainder=False
        )
        
        
    def get_player_with_least_points(self):
        '''Get the player which has the lowest number of points.'''
        return min(self.players, key=lambda player: player.points)

    
    def get_n_players_of_given_type(self, player_type):
        '''Get the number of existing players of the type `player_type`.'''
        return len([player for player in self.players
                    if isinstance(player, player_type)])


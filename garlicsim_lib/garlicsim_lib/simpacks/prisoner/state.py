# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Simpack for a repeating game of prisoner's dillema with natural selection.
'''

import random
random.seed()

import garlicsim.data_structures

from .player import Player
from .players import player_types_list


class State(garlicsim.data_structures.State):
    
    def __init__(self, round, match, player_pool, n_rounds=7):
        self.round = round
        self.match = match
        self.player_pool = player_pool
        self.n_rounds = n_rounds
        
    
    @staticmethod
    def create_root(n_players=70, n_rounds=7):
        global player_types
        state = State(
            round=-1,
            match=0,
            player_pool=[
                player_types[i % len(player_types)]() for \
                i in xrange(n_players)
            ],
            n_rounds=n_rounds
        )
        state.prepare_for_new_match()
        return state
    
    
    @staticmethod
    def create_messy_root(n_players=70, n_rounds=7):
        global player_types
        state = State(
            round=-1,
            match=0,
            player_pool=[random_strategy_player() for i in xrange(n_players)],
            n_rounds=n_rounds
        )
        state.prepare_for_new_match()
        return state
    
        
    def inplace_step(self):
        self.clock += 1
    
        self.round += 1
        if self.round == self.n_rounds:
            self.round = -1
            self.match += 1
            self.prepare_for_new_match()
            return
    
        for pair in self.pairs:
            play_game(pair, self.round)
    
    
    def prepare_for_new_match(self):
        '''
        Note: this function is not strictly a "step function":
        it manipulates the state that is given to it and then returns it.
        '''
        pool = self.player_pool
        loser = player_with_least_points(pool)
        pool.remove(loser)
        pool.append(random_strategy_player())
    
        self.pairs = pair_pool(self.player_pool)



def pair_pool(player_pool):
    '''
    Takes a player pool and returns a list of random pairs of players.
    Every player will be a member of exactly one pair.
    '''
    assert len(player_pool) % 2 == 0
    result = []
    pool = player_pool[:]
    while len(pool) > 0:
        pair = random.sample(pool, 2)
        result.append(pair)
        pool.remove(pair[0])
        pool.remove(pair[1])
    return result

def play_game((x, y), round):
    x_move = x.play(round)
    y_move = y.play(round)

    assert x_move in [True, False]
    assert y_move in [True, False]

    if x_move == True and y_move == True:
        x.points += 1
        y.points += 1
    elif x_move == True and y_move == False:
        x.points += -4
        y.points += 2
    elif x_move == False and y_move == True:
        x.points += 2
        y.points += -4
    elif x_move == False and y_move == False:
        x.points += -1
        y.points += -1

    x.other_player_played(y_move)
    y.other_player_played(x_move)

def random_strategy_player():
    player = random.choice(player_types)
    return player()



    



player_types = [Angel, Devil, TitForTat]

def how_many_players_of_certain_type(pool, type):
    n = 0
    for player in pool:
        if isinstance(player, type):
            n += 1
    return n

def player_with_least_points(pool):
    assert len(pool) > 0
    loser = pool[0]
    for player in pool:
        if player.points < loser.points:
            loser = player
    return loser


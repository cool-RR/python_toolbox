# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `TitForTat` player type.

See its documentation for more information.
'''

from ..base_player import BasePlayer


class TitForTat(BasePlayer):
    '''
    Player which plays nice on the 1st round and afterwards imitates opponent.
    
    On the first round this player will always play nice. On every subsequent
    round, it will play the move that the opponent played on the previous
    round.
    
    This is a good strategy, because it allows the `TitForTat` player to
    cooperate with other `TitForTat` players and with `Angel` players, but it
    doesn't let any `Devil` players exploit it.
    '''
    
    color = 'Blue'
    
    def make_move(self, round):
        '''Play nice on 1st round, afterwards imitate opponent.'''
        if round == 0:
            self.last_play = None
            return True
        else:
            return self.last_play

    def other_player_played(self, move):
        '''Save the opponent's move so we can do the same on the next round.'''
        self.last_play = move


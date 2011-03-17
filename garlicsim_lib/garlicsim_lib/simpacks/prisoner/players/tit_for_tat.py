# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `TitForTat` player type.

See its documentation for more information.
'''

from ..player import BasePlayer


class TitForTat(BasePlayer):
    
    color = 'Blue'
    
    def play(self, round):
        if round == 0:
            return True
        else:
            return self.last_play

    def other_player_played(self, move):
        self.last_play = move


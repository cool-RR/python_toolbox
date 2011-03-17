# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `Player` class.

See its documentation for more information.
'''

class Player(object):
    def __init__(self):
        self.points = 0

    def play(self, *args, **kwargs):
        raise NotImplementedError

    def other_player_played(self,move):
        pass
    
    @staticmethod
    def create_random_strategy_player():
        player = random.choice(player_types_list)
        return player()
# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `BasePlayer` abstact base class.

See its documentation for more information.
'''

from garlicsim.general_misc.third_party import abc

from garlicsim.general_misc import identities

from .player_type import PlayerType


class BasePlayer(identities.HasIdentity):
    '''
    A player that plays prisoner's dilemma, gaining and losing points.
    
    This is an abstract base class; subclass this to implement actual playing
    strategies.
    '''
    
    __metaclass__ = PlayerType

    color = None
    '''
    Name of color that will represent this player class in a GUI. Optional.
    '''
        
    def __init__(self):
        identities.HasIdentity.__init__(self)
        
        self.points = 0
        '''The number of points that the player has.'''
        
        
    @abc.abstractmethod
    def make_move(self, round):
        '''
        Decide which move to make.
        
        Abstract method.
        
        `round` is the round number in the match, starting with 0.
        
        Note that no information about the other player is given to this
        method. Any state that a player subclass wants to have should be
        created by it and saved as data attributes to the player instance.
        
        Returns a boolean, `True` is "be nice" and `False` is "be mean".
        '''
        
    
    def other_player_played(self, move):
        '''
        The other player played `move` in the last round.
        
        A player subclass may implement here something that saves this move and
        takes it into account on subsequent rounds.
        '''
        pass
    
    
    def play_game(player_1, player_2, round):
        '''
        Have `player_1` and `player_2` play against each other.
        
        Each player will gain or lose points according to the outcome of the
        game.
        '''        
        assert isinstance(player_1, BasePlayer)
        assert isinstance(player_2, BasePlayer)
    
        player_1_move = player_1.make_move(round)
        player_2_move = player_2.make_move(round)
    
        assert isinstance(player_1_move, bool)
        assert isinstance(player_2_move, bool)
    
        ### Calculating outcome of game in points for each player: ############
        #                                                                     #
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
        #                                                                     #
        ### Finished calculating outcome of game in points for each player. ###
    
        player_1.other_player_played(player_2_move)
        player_2.other_player_played(player_1_move)
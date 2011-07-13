# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Simpack for a repeated game of Prisoner's Dilemma with natural selection.

The `Prisoner's Dilemma`_ is probably the most famous game in `Game Theory`_.
Two players play against each other. Each of them can either "play nice" or
"play mean". If both play nice, both of them gain points, a.k.a "cooperation".
If both play mean, both lose points. If one plays mean while the other plays
nice, the mean one gets a lot of points while the nice one loses a lot of
points, a.k.a "exploitation".

A `repeated game`_ in Game Theory is when players play the same game repeatedly
for many rounds. After every round they discover what the other player played
in that round. A repeated game allows for many interesting phenomena not seen
in one-off games, like players punishing their opponents for playing mean in
previous rounds.

In this simpack, a pool of players of different strategies get paired randomly
and play a repeated game of Prisoner's Dilemma against each other. After a
multi-round match is finished, they get randomly assigned a new opponent and
play another match. In this phase we introduce some `natural selection`_ as the
player with the least points gets kicked out and replaced with a new player of
a random type.

As the players keep playing more and more matches, we can observe the how
distribution of the population into different player types changes over time.

.. _Prisoner's Dilemma: http://en.wikipedia.org/wiki/Prisoner's_dilemma
.. _Game Theory: http://en.wikipedia.org/wiki/Game_Theory
.. _repeated game: http://en.wikipedia.org/wiki/Repeated_game
.. _natural selection: http://en.wikipedia.org/wiki/Natural_selection

'''

from .state import State
from .base_player import BasePlayer

name = "Prisoner's Dilemma"

tags = ('game-theory', "prisoner's-dilemma", 'repeated-game')
# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
A simpack for Conway's Game of Life.

`Conway's Game of Life`_, also known as Life, is a `cellular automaton`_.

The universe of the Game of Life is an infinite two-dimensional grid of square
cells, each of which may be either dead (white) or alive (black). At each turn
of the simulation, the following transitions occur:

    - Any live cell with fewer than two live neighbors becomes dead.
    
    - Any live cell with two or three live neighbors continues to be alive.
    
    - Any live cell with more than three live neighbors becomes dead.
    
    - Any dead cell with exactly three live neighbors becomes alive.
    
Out of the simple rules of the Life universe, one can observe `many complex and
interesting "life forms"`_ emerge.

.. _Conway's Game of Life: http://en.wikipedia.org/wiki/Conway's_Game_of_Life
.. _cellular automaton: http://en.wikipedia.org/wiki/Cellular_automaton
.. _many complex and interesting "life forms": http://en.wikipedia.org/wiki/Conway's_Game_of_Life#Examples_of_patterns
'''

from .state import State
    
name = "Conway's Game of Life"

tags = ('cellular-automata', "conway's-game-of-life", 'abstract')

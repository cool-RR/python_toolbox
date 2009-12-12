# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
tododoc
'''

import random

import garlicsim.data_structures
from garlicsim.misc import Persistent

from vectors import Vector

class State(garlicsim.data_structures.State):
    def __init__(self, particles):
        self.particles = list(particles)
    
def step(old_state, useless=None, krazy=None):
    old_board = old_state.board
    new_board = Board(parent=old_board)
    new_state = State()
    if krazy:
        new_state.board = \
            Board(old_board.width, old_board.height, fill='random')
        return new_state
    new_state.board = new_board
    return new_state

'''
def make_plain_state(width=45, height=25, fill="empty"):
    my_state = State()
    my_state.board = Board(width, height, fill)
    return my_state
'''

def make_random_state():
    big_random_number = lambda: random.uniform(-100, 100)
    small_random_number = lambda: random.uniform(-10, 10)
    big_random_vector = lambda: Vector((big_random_number() for i in range(3)))
    small_random_vector = lambda: Vector((small_random_number() for i in range(3)))
    
    random_particle = lambda: Particle(position=big_random_vector(), velocity=small_random_vector(), mass=1, charge=small_random_number())
    
    particles = (random_particle() for i in range(5))
    my_state = State(particles=particles)
    return my_state

class Particle(object):

    def __init__(self, position=None, velocity=None, mass=1, charge=1):
        self.position = position or Vector((0, 0, 0))
        self.velocity = velocity or Vector((0, 0, 0))
        self.mass = mass
        self.charge = charge
        self.identity = Persistent
    
    def make_acceleration(self):
        
        
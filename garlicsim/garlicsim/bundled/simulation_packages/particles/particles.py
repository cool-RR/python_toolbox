# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
tododoc
'''

import random
import copy

import garlicsim
import garlicsim.data_structures
from garlicsim.misc import Persistent

from vectors import Vector

ke = 8987551787.3681764


class State(garlicsim.data_structures.State):
    def __init__(self, particles):
        self.particles = list(particles)
    
def step(old_state, t=1):

    new_state = copy.deepcopy(old_state)
    new_state.clock += t
    
    '''
    old_particles_dict = dict([(new_particle, [particle for particle in old_state.particles if particle.identity is new_particle_identity][0]) for new_particle in new_state.particle])
    '''
    '''Mapping from the particles of the new state to their original sources.'''
    
    for particle in new_state.particles:
        other_old_particles = (p for p in old_state.particles if p.identity is not particle.identity)
        force_sum = Vector((0, 0, 0))
        for other_particle in other_old_particles:
            other_force = particle - other_particle
            force_sum += other_force
        
        new_acceleration = force_sum / particle.mass
        average_acceleration = (new_acceleration + particle.acceleration) / 2
        new_velocity = particle.acceleration * t + particle.velocity
        average_velocity = (new_velocity + particle.velocity) / 2
        new_position = average_velocity * t + particle.position
        
        particle.position = new_position
        particle.velocity = new_velocity
        particle.acceleration = new_acceleration
        
    
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


#####################################################

from enthought.traits.api import HasTraits, Float, Instance, Range

class Particle(HasTraits):

    position = Instance(Vector, args=((0, 0, 0),), allow_none=False)
    velocity = Instance(Vector, args=((0, 0, 0),), allow_none=False)
    acceleration = Instance(Vector, args=((0, 0, 0),), allow_none=False)
    mass = Range(low=0, exclude_low=True)
    charge = Float
    
    def __init__(self, *args, **kwargs):
        HasTraits.__init__(self, *args, **kwargs)
        self.identity = Persistent
        
        
    def __sub__(self, other):
        '''Force from other particle on this one.'''
        assert isinstance(other, Particle)
        vector_to_self = self.position - other.position
        distance = abs(vector_to_self)
        return (ke * self.charge * other.charge / (distance ** 3)) * vector_to_self
    
    def __rsub__(self, other):
        return other.__sub__(self)
    

    def __repr__(self):
        return 'Position: ' + repr(self.position)
        
        
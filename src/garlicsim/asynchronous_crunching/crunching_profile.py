# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

"""
This module defines the CrunchingProfile class. See its documentation for more
information.
"""

class CrunchingProfile(object):
    '''
    A crunching profile is a set of instructions that a cruncher follows when
    crunching the simulation.
    '''
    def __init__(self, clock_target=None, step_options_profile=None):
        
        self.clock_target = clock_target
        '''
        This says we want the cruncher to crunch until it gets a state with a
        clock of `.clock_target` or higher.
        '''
        
        self.step_options_profile = step_options_profile
        '''
        The step options profile we want to be used with the step function.
        '''
  
    def state_satisfies(self, state):
        '''
        Checks whether a state has a clock high enough to satisfy this profile.
        '''
        return state.clock >= self.clock_target
    
    def __eq__(self, other):
        return isinstance(other, CrunchingProfile) and \
               self.clock_target == other.clock_target and \
               self.step_options_profile == other.step_options_profile
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __repr__(self):
        stuff = []
        stuff.append("clock_target=%s" % self.clock_target)
        stuff.append("step_options_profile=%s" % self.step_options_profile)
        temp = ", ".join(stuff)
        return ("CrunchingProfile(%s)" % temp)
    
    
    
    
    
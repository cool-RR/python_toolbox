# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

"""
tododoc
"""

__all__ = ['Job']

class Job(object): # rename to job
    '''
    TODODOC
    A crunching profile is a set of instructions that a cruncher follows when
    crunching the simulation.
    '''
    def __init__(self, node, crunching_profile):
        
        self.node = node
        
        self.crunching_profile = crunching_profile
  
    
    def is_done(self):
        '''
        does not check the node's leaf!
        '''
        return node.state.clock >= self.crunching_profile.clock_target
    
    # todo: should there be an is_done here or other helpful methods?
        
    # todo: make __repr__ like this:
    """
    def __repr__(self):
        stuff = []
        stuff.append("clock_target=%s" % self.clock_target)
        stuff.append("step_options_profile=%s" % self.step_options_profile)
        temp = ", ".join(stuff)
        return ("CrunchingProfile(%s)" % temp)
    """
    
    
    
    
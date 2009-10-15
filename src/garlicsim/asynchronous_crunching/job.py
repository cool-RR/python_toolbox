# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

"""
This module defines the Job class. See its documentation for more info.
"""

__all__ = ['Job']

class Job(object): # rename to job
    '''
    A job of crunching the simulation from a given node.
        
    A job specifies a node and a crunching profile. It means we should crunch
    from node according to the cruncing profile.
    '''
    def __init__(self, node, crunching_profile):
        
        self.node = node
        '''
        The node from which we need to crunch.
        '''
        
        self.crunching_profile = crunching_profile
        '''
        The crunching profile to be used for crunching.
        '''
  
    def is_done(self):
        '''
        Return whether the job is done, i.e. enough crunching has been done.
        '''
        return self.crunching_profile.state_satisfies(self.node.state)
    
    # todo: should there be other helpful methods here?
        
    # todo: make __repr__ like this:
    
    def __repr__(self): #todo: ensure not subclass?
        stuff = []
        stuff.append("node=%s" % self.node)
        stuff.append("crunching_profile=%s" % self.crunching_profile)
        temp = ", ".join(stuff)
        return ("Job(%s)" % temp)
    
    
    
    
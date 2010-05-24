# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the Job class.

See its documentation for more info.
'''

__all__ = ['Job']

class Job(object):
    '''
    A job of crunching the simulation from a given node.
        
    A job specifies a node and a crunching profile. It means we should crunch
    from `node` according to the cruncing profile.
    '''
    # todo: should there be other helpful methods here?
    
    def __init__(self, node, crunching_profile):
        
        self.node = node
        '''The node from which we need to crunch.'''
        
        self.crunching_profile = crunching_profile
        '''The crunching profile to be used for crunching.'''
        
        self.resulted_in_end = False
        '''Flag marking that the job has resulted in an end of the simulation.'''
  
        
    def is_done(self):
        '''
        Return whether the job is done, i.e. enough crunching has been done.
        '''
        return self.crunching_profile.state_satisfies(self.node.state) or \
               self.resulted_in_end
    
        
    def __repr__(self): #todo: ensure not subclass?
        '''
        Get a string representation of the job.
        
        Example output: 

        Job(node=<garlicsim.data_structures.node.Node with clock 17, untouched,
        belongs to a block, crunched with StepProfile(), at 0x20664b0>,
        crunching_profile=CrunchingProfile(clock_target=100,
        step_profile=StepProfile()))
        '''
        
        stuff = []
        stuff.append("node=%s" % self.node)
        stuff.append("crunching_profile=%s" % self.crunching_profile)
        temp = ", ".join(stuff)
        return ("Job(%s)" % temp)
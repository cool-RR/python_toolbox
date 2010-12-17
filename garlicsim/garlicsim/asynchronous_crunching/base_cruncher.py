# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the BaseCruncher class.

See its documentation for more information. See the `crunchers` package for a
collection of crunchers.
'''

import copy

from garlicsim.general_misc.third_party import abc

from garlicsim.general_misc import abc_tools

import garlicsim


class BaseCruncher(object):
    '''
    
    
    A cruncher receives a state from the main program, and then it repeatedly
    applies the step function of the simulation to produce more states. Those
    states are then put in the cruncher's `.work_queue`. They are then taken by
    the main program when `Project.sync_crunchers` is called, and put into the
    tree.

    The cruncher also receives a crunching profile from the main program. The
    crunching profile specifes how far the cruncher should crunch the
    simulation, and which arguments it should pass to the step function.
    
    This package may define different crunchers which work in different ways,
    but are to a certain extent interchangable. Different kinds of crunchers
    have different advantages and disadvantges relatively to each other, and
    which cruncher you should use for your project depends on the situation.
    '''
    
    __metaclass__ = abc.ABCMeta

    
    gui_explanation = None

    
    def __init__(self, crunching_manager, initial_state, crunching_profile):
        
        self.crunching_manager = crunching_manager
        assert isinstance(self.crunching_manager,
                          garlicsim.asynchronous_crunching.CrunchingManager)
        
        self.project = crunching_manager.project
        assert isinstance(self.project, garlicsim.Project)
        
        self.initial_state = initial_state
        assert isinstance(self.initial_state, garlicsim.data_structures.State)
        
        self.crunching_profile = copy.deepcopy(crunching_profile)
        assert isinstance(self.crunching_profile,
                          garlicsim.asynchronous_crunching.CrunchingProfile)
        
    
    @abc_tools.abstract_static_method
    def can_be_used_with_simpack_grokker(simpack_grokker):
        '''
        Return whether this cruncher type can be used with a simpack grokker.
        '''
        '''
        
        (Static method.)
        '''
        
    
    @abc.abstractmethod
    def retire(self):
        '''Retire the cruncher, making it shut down.'''
    
    
    @abc.abstractmethod
    def update_crunching_profile(self, profile):
        '''Update the cruncher's crunching profile.'''
        
    
    @abc.abstractmethod
    def is_alive(self):
        '''Report whether the cruncher is alive and crunching.'''
        
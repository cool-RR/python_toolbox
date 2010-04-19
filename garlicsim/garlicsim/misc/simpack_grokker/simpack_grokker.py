# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the SimpackGrokker class and the InvalidSimpack exception.

See their documentation for more details.
'''

import functools
import types

from garlicsim.misc import AutoClockGenerator, StepIterator, InvalidSimpack
import garlicsim

import misc

__all__ = ["SimpackGrokker"]

class Settings(object):
    #todo: subclass from a pretty vars-shower
    def __init__(self):
        self.FORCE_CRUNCHER = None
        self.DETERMINISM_FUNCTION = misc.default_determinism_function
        self.SCALAR_STATE_FUNCTIONS = []
        self.SCALAR_HISTORY_FUNCTIONS = []

class SimpackGrokker(object):
    '''
    An object that encapsulates a simpack, giving useful information about it
    and tools to use with it.
    
    todo: move this somewhere else:
    
    class Meta:
    
        deterministic = garlicsim.misc.constants.UNDETERMINISTIC
        
        # Says whether the step function of this simpack is deterministic. This
        # is useful because if a simpack declares itself to be deterministic
        # then GarlicSim can analyze whether a simulation has reached a
        # constant/repetitive state.
        
        # UNDETERMINISTIC means completely not deterministic -- has a random
        # element.
        
        # SUPPOSEDLY_DETERMINISTIC means deterministic in principle, but not
        # absolutely. (For example, in some simpacks rounding errors may make
        # states that should otherwise be equal not be equal.)
        
        # DETERMINISTIC means absolutely deterministic. There is no random
        # element in the step function, and given identical input states it is
        # guaranteed to return identical output states.
        
        ################################################
        
        scalar_state_functions = [live_cells, maturity]
        
        # List of scalar state functions given by the simpack. A scalar state
        # function is a function from a state to a real number. These should be
        # decorated by garlicsim.misc.cached.state_cache.
        
        scalar_history_functions = [changes]
        
        # List of scalar history functions given by the simpack. A scalar
        # history function is a function from a history browser to a real
        # number. These should be decorated by
        # garlicsim.misc.cached.history_cache.
        
        ################################################
        
        (tododoc: The following belong in Meta_wx, move it)
        
        seek_bar_graphs = [live_cells, changes]
        
        # List of scalar state function and scalar history functions that should
        # be shown as graphs in the seek bar.
        
        ################################################
        
    '''
    def __init__(self, simpack):
        self.simpack = simpack
        self.__init_analysis()
        self.__init_analysis_settings()
    
    def __init_analysis(self):
        '''Analyze the simpack.'''
        simpack = self.simpack

        self.simple_non_history_step_defined = hasattr(simpack, "step")
        self.non_history_step_generator_defined = \
            hasattr(simpack, "step_generator")
        self.simple_history_step_defined = hasattr(simpack, "history_step")
        self.history_step_generator_defined = hasattr(simpack,
                                                      "history_step_generator")
        
        self.non_history_step_defined = \
            (self.simple_non_history_step_defined or \
             self.non_history_step_generator_defined)
        
        self.history_step_defined = (self.simple_history_step_defined or \
                                     self.history_step_generator_defined)
        
        self.simple_step_defined = (self.simple_non_history_step_defined or \
                                    self.simple_history_step_defined)
        
        self.step_generator_defined = \
            (self.non_history_step_generator_defined or \
             self.history_step_generator_defined)
        
        if self.history_step_defined and self.non_history_step_defined:
            raise InvalidSimpack('''The simulation package is defining both a \
history-dependent step and a non-history-dependent step - which is forbidden.\
''')
        
        if not (self.simple_step_defined or self.step_generator_defined):
            raise InvalidSimpack('''The simulation package has not defined any \
kind of step function.''')
        
        self.history_dependent = self.history_step_defined
        
    
    def __init_analysis_settings(self):
        #tododoc
        
        # We want to access the `.settings` of our simpack, but we don't know if
        # our simpack is a module or some other kind of object. So if it's a
        # module, we'll `try` to import `settings`.
        
        self.settings = Settings()        
        
        if isinstance(self.simpack, types.ModuleType):
            try:
                __import__(''.join((self.simpack.__name__, '.settings')))
                # This imports the `settings` submodule, but does *not* keep a
                # reference to it. We'll access it as an attribute of the
                # simpack below.
            
            except ImportError:
                pass
            
        # Checking if there are original settings at all. If there aren't, we're
        # done.
        if hasattr(self.simpack, 'settings'):
            
            original_settings = getattr(self.simpack, 'settings')
        
            for (key, value) in vars(self.settings).iteritems():
                if hasattr(original_settings, key):
                    actual_value = getattr(original_settings, key)
                    setattr(self.settings, key, actual_value)
            # todo: currently throws away unrecognized attributes from the
            # simpack's settings.
                
        
    def step(self, state_or_history_browser, step_profile):
        '''
        Perform a step of the simulation.
        
        The step profile will specify which parameters to pass to the simpack's
        step function.
        '''
        auto_clock_generator = AutoClockGenerator()
        if isinstance(state_or_history_browser,
                      garlicsim.data_structures.State):
            state = state_or_history_browser
        else:
            state = state_or_history_browser.get_last_state()
        auto_clock_generator.make_clock(state)

        if self.simple_step_defined:
            step_function = self.simpack.history_step if \
                          self.history_dependent else self.simpack.step
            result = step_function(state_or_history_browser,
                                   *step_profile.args,
                                   **step_profile.kwargs)
        else: # self.step_generator_defined is True
            step_generator = self.simpack.history_step_generator if \
                          self.history_dependent else \
                          self.simpack.step_generator
            iterator = step_generator(state_or_history_browser,
                                      *step_profile.args,
                                      **step_profile.kwargs)
            result = iterator.next()
            
        result.clock = auto_clock_generator.make_clock(result)
        return result
            
        
    
    def step_generator(self, state_or_history_browser, step_profile):
        '''
        Step generator for crunching states of the simulation.
        
        The step profile will specify which parameters to pass to the simpack's
        step function.
        '''
        
        if self.step_generator_defined:
            step_generator = self.simpack.history_step_generator if \
                           self.history_dependent else \
                           self.simpack.step_generator
            return StepIterator(state_or_history_browser, step_profile,
                                step_generator=step_generator)
        else:
            assert self.simple_step_defined
            simple_step = self.simpack.history_step if self.history_dependent \
                        else self.simpack.step
            return StepIterator(state_or_history_browser, step_profile,
                                simple_step=simple_step)
        
        
        

# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the SimpackGrokker class and the InvalidSimpack exception.

See their documentation for more details.
'''

import functools
import types
import imp

from garlicsim.general_misc import import_tools
import garlicsim.general_misc.caching

from garlicsim.misc import (AutoClockGenerator, StepIterator, InvalidSimpack,
                            simpack_tools)
import misc

from .settings import Settings


class SimpackGrokker(object):
    '''Encapsulates a simpack and gives useful information and tools.'''
    
    __metaclass__ = garlicsim.general_misc.caching.CachedType

    @staticmethod
    def create_from_state(state):
        simpack = simpack_tools.get_from_state(state)
        return SimpackGrokker(simpack)
    
    
    def __init__(self, simpack):
        self.simpack = simpack
        self.__init_analysis()
        self.__init_analysis_settings()

        
    def __init_analysis(self):
        '''Analyze the simpack.'''
        
        simpack = self.simpack
        
        try:
            State = simpack.State
        except AttributeError:
            raise InvalidSimpack('''The %s simpack does not define a `State` \
class.''' % simpack.__name__)
        
        if not issubclass(State, garlicsim.data_structures.State):
            raise InvalidSimpack('''The %s simpack defines a State class, but \
it's not a subclass of `garlicsim.data_structures.State`.''' % \
                                                             simpack.__name__)

        self.simple_non_history_step_defined = hasattr(State, "step")
        self.non_history_step_generator_defined = \
            hasattr(State, "step_generator")
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
            raise InvalidSimpack('''The %s simpack is defining both a \
history-dependent step and a non-history-dependent step - which is forbidden.\
''' % simpack.__name__)
        
        if not (self.simple_step_defined or self.step_generator_defined):
            raise InvalidSimpack('''The %s simpack has not defined any kind \
of step function.''' % simpack.__name__)
        
        self.history_dependent = self.history_step_defined
        
    
    def __init_analysis_settings(self):
        '''Analyze the simpack to produce a Settings object.'''
        # todo: consider doing this in Settings.__init__
        
        # We want to access the `.settings` of our simpack, but we don't know if
        # our simpack is a module or some other kind of object. So if it's a
        # module, we'll `try` to import `settings`.
        
        self.settings = Settings()        
        
        if isinstance(self.simpack, types.ModuleType) and \
           not hasattr(self.simpack, 'settings'):
            
            # The `if` that we did here means: "If there's reason to suspect
            # that self.simpack.settings is a module that exists but hasn't been
            # imported yet."
            
            settings_module_name = ''.join((
                self.simpack.__name__,
                '.settings'
            ))
            
            import_tools.import_if_exists(settings_module_name)
            # This imports the `settings` submodule, if it exists, but it
            # does *not* keep a reference to it. We'll access `settings` as
            # an attribute of the simpack below.
            
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
                          self.history_dependent else self.simpack.State.step
            result = step_function(state_or_history_browser,
                                   *step_profile.args,
                                   **step_profile.kwargs)
        else: # self.step_generator_defined is True
            step_generator = self.simpack.history_step_generator if \
                          self.history_dependent else \
                          self.simpack.State.step_generator
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
                           self.simpack.State.step_generator
            return StepIterator(state_or_history_browser, step_profile,
                                step_generator=step_generator)
        else:
            assert self.simple_step_defined
            simple_step = self.simpack.history_step if self.history_dependent \
                        else self.simpack.State.step
            return StepIterator(state_or_history_browser, step_profile,
                                simple_step=simple_step)
        
        
        

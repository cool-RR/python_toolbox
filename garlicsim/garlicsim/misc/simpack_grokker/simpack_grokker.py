# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the SimpackGrokker class and the InvalidSimpackblocktododoc exception.

See their documentation for more details.
'''

import functools
import types
import imp

from garlicsim.general_misc import import_tools
from garlicsim.general_misc import misc_tools
from garlicsim.general_misc import cute_iter_tools
from garlicsim.general_misc import sequence_tools
from garlicsim.general_misc.reasoned_bool import ReasonedBool
from garlicsim.general_misc.third_party.ordered_dict import OrderedDict
import garlicsim.general_misc.caching

from garlicsim.misc import (AutoClockGenerator, InvalidSimpack,
                            GarlicSimException, simpack_tools)
from garlicsim.misc import step_iterators as step_iterators_module
from . import misc

from .settings import Settings
from .get_step_type import get_step_type
from . import step_types


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
        self.__init_analysis_cruncher_types()

        
    def __init_analysis(self):
        '''Analyze the simpack.'''
        
        simpack = self.simpack
        
        try:
            State = simpack.State
        except AttributeError:
            raise InvalidSimpack("The `%s` simpack does not define a `State` "
                                 "class." % simpack.__name__.rsplit('.')[-1])
        
        if not misc_tools.is_subclass(State, garlicsim.data_structures.State):
            raise InvalidSimpack("The `%s` simpack defines a State class, but "
                                 "it's not a subclass of "
                                 "`garlicsim.data_structures.State`." % \
                                 simpack.__name__.rsplit('.')[-1])


        state_methods = dict(
            (name, value) for (name, value) in
            misc_tools.getted_vars(State).iteritems() if callable(value)
        )

        self.step_functions_by_type = dict((step_type, []) for step_type in
                                           step_types.step_types_list)
        
        
        for method in state_methods.itervalues():
            if 'step' in method.__name__:
                step_type = get_step_type(method)
                self.step_functions_by_type[step_type].append(method)
            
                
        if self.step_functions_by_type[step_types.HistoryStep] or \
           self.step_functions_by_type[step_types.HistoryStepGenerator]:
            
            self.history_dependent = True

            self.all_step_functions = (
                self.step_functions_by_type[step_types.HistoryStepGenerator] + \
                self.step_functions_by_type[step_types.HistoryStep]
            )
            
            if self.step_functions_by_type[step_types.SimpleStep] or \
               self.step_functions_by_type[step_types.StepGenerator] or \
               self.step_functions_by_type[step_types.InplaceStep] or \
               self.step_functions_by_type[step_types.InplaceStepGenerator]:
                
                raise InvalidSimpack("The `%s` simpack is defining both a "
                                     "history-dependent step and a "
                                     "non-history-dependent step - which "
                                     "is forbidden." % \
                                     simpack.__name__.rsplit('.')[-1])
        else: # No history step defined
            
            self.history_dependent = False
            
            self.all_step_functions = (
                self.step_functions_by_type[step_types.StepGenerator] + \
                self.step_functions_by_type[step_types.SimpleStep] + \
                self.step_functions_by_type[step_types.InplaceStepGenerator] +\
                self.step_functions_by_type[step_types.InplaceStep]
            )
            
        self.all_step_functions = self.all_step_functions # (Just for docs.)
        '''
        
        Sorted by priority.
        '''
               
        if not self.all_step_functions:
            raise InvalidSimpack("The `%s` simpack has not defined any kind "
                                 "of step function." % \
                                 simpack.__name__.rsplit('.')[-1])
        
        self.default_step_function = self.all_step_functions[0]
        ''' '''
        
        
    
    def __init_analysis_settings(self):
        '''Analyze the simpack to produce a Settings object.'''
        # todo: consider doing this in Settings.__init__
        
        # We want to access the `.settings` of our simpack, but we don't know if
        # our simpack is a module or some other kind of object. So if it's a
        # module, we'll `try` to import `settings`.
        
        self.settings = Settings(self)
        
        if isinstance(self.simpack, types.ModuleType) and \
           not hasattr(self.simpack, 'settings'):
            
            # The `if` that we did here means: "If there's reason to suspect
            # that self.simpack.settings is a module that exists but hasn't been
            # imported yet."
            
            settings_module_name = ''.join((
                self.simpack.__name__.rsplit('.')[-1],
                '.settings'
            ))
            
            import_tools.import_if_exists(settings_module_name,
                                          silent_fail=True)
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
                

    def __init_analysis_cruncher_types(self):
        
        # todo: possibly fix CRUNCHERS to some canonical state in `.settings`
        from garlicsim.asynchronous_crunching import crunchers, BaseCruncher
        simpack = self.simpack
        
        self.cruncher_types_availability = OrderedDict()
        
        CRUNCHERS = self.settings.CRUNCHERS

        
        if isinstance(CRUNCHERS, basestring):
            (cruncher_type,) = \
                [cruncher_type_ for cruncher_type_ in
                 crunchers.cruncher_types_list if
                 cruncher_type_.__name__ == CRUNCHERS]
            self.available_cruncher_types = [cruncher_type]
            self.cruncher_types_availability[cruncher_type] = True
        
            ### Giving unavailability reasons: ################################
            #                                                                 #
            unavailable_cruncher_types = \
                [cruncher_type_ for cruncher_type_ in
                 crunchers.cruncher_types_list if cruncher_type_ not in
                 self.available_cruncher_types]
            self.cruncher_types_availability.update(dict(
                (
                    unavailable_cruncher_type,
                    ReasonedBool(
                        False,
                        'The `%s` simpack specified `%s` as the only '
                        'available cruncher type' % \
                        (simpack.__name__.rsplit('.')[-1],
                         cruncher_type.__name__)
                    )
                ) for unavailable_cruncher_type in unavailable_cruncher_types
            ))
            #                                                                 #
            ###################################################################

        
        elif misc_tools.is_subclass(CRUNCHERS, BaseCruncher):
            cruncher_type = CRUNCHERS
            self.available_cruncher_types = [cruncher_type]
            self.cruncher_types_availability[cruncher_type] = True
            
            ### Giving unavailability reasons: ################################
            #                                                                 #
            unavailable_cruncher_types = \
                [cruncher_type_ for cruncher_type_ in
                 crunchers.cruncher_types_list if cruncher_type_ not in
                 self.available_cruncher_types]
            self.cruncher_types_availability.update(dict(
                (
                    unavailable_cruncher_type,
                    ReasonedBool(
                        False,
                        'The `%s` simpack specified `%s` as the only '
                        'available cruncher type' % (simpack.__name__.rsplit('.')[-1],
                                                     cruncher_type.__name__)
                    )
                ) for unavailable_cruncher_type in unavailable_cruncher_types
            ))
            #                                                                 #
            ###################################################################
            
        
        elif cute_iter_tools.is_iterable(CRUNCHERS):
            self.available_cruncher_types = []
            for item in CRUNCHERS:
                if isinstance(item, basestring):
                    (cruncher_type,) = \
                        [cruncher_type_ for cruncher_type_ in
                         crunchers.cruncher_types_list if
                         cruncher_type_.__name__ == item]
                else:
                    assert misc_tools.is_subclass(item, BaseCruncher)
                    cruncher_type = item
                self.available_cruncher_types.append(cruncher_type)
                self.cruncher_types_availability[cruncher_type] = True

            ### Giving unavailability reasons: ################################
            #                                                                 #
            unavailable_cruncher_types = \
                [cruncher_type_ for cruncher_type_ in
                 crunchers.cruncher_types_list if cruncher_type_ not in
                 self.available_cruncher_types]
            self.cruncher_types_availability.update(dict(
                (
                    unavailable_cruncher_type,
                    ReasonedBool(
                        False,
                        'The `%s` simpack specified a list of available '
                        'crunchers and `%s` is not in it.' % \
                        (simpack.__name__.rsplit('.')[-1],
                         unavailable_cruncher_type.__name__)
                    )
                        
                ) for unavailable_cruncher_type in unavailable_cruncher_types
            ))
            #                                                                 #
            ###################################################################
            
        
        elif callable(CRUNCHERS):
            assert not isinstance(CRUNCHERS, BaseCruncher)
            self.available_cruncher_types = \
                [cruncher_type_ for cruncher_type_ in
                 crunchers.cruncher_types_list if
                 CRUNCHERS(cruncher_type_)]
            for available_cruncher_type in self.available_cruncher_types:
                self.cruncher_types_availability[available_cruncher_type] = \
                    True
            
            ### Giving unavailability reasons: ################################
            #                                                                 #
            unavailable_cruncher_types = \
                [cruncher_type_ for cruncher_type_ in
                 crunchers.cruncher_types_list if cruncher_type_ not in
                 self.available_cruncher_types]
            for unavailable_cruncher_type in unavailable_cruncher_types:
                reason = getattr(
                    CRUNCHERS(unavailable_cruncher_type),
                    'reason',
                    'No reason was given for `%s` not being accepted.' % \
                    unavailable_cruncher_type.__name__
                )
                self.cruncher_types_availability[
                    unavailable_cruncher_type
                    ] = ReasonedBool(False, reason)
            #                                                                 #
            ###################################################################
            
        #######################################################################
            
        else:
            raise InvalidSimpack("The `CRUNCHERS` setting must be either a "
                                 "cruncher type (or name string), a list of "
                                 "cruncher types, or a filter function for "
                                 "cruncher types. You supplied `%s`, which is "
                                 "neither." % CRUNCHERS)
            
    
    def step(self, state_or_history_browser, step_profile):
        '''
        Perform a step of the simulation.
        
        The step profile will specify which parameters to pass to the simpack's
        step function.
        '''
    
        # todo: probably inefficient, but this method is probably not used much
        # anyway.
        
        step_iterator = self.get_step_iterator(state_or_history_browser,
                                               step_profile)
        return step_iterator.next()
    
            
    def get_step_iterator(self, state_or_history_browser, step_profile):
        '''
        Step generator for crunching states of the simulation.
        
        The step profile will specify which parameters to pass to the simpack's
        step function.
        '''
        
        step_function = step_profile.step_function
        step_type = get_step_type(step_function)
        step_iterator_class = step_type.step_iterator_class

        step_iterator = step_iterator_class(state_or_history_browser,
                                            step_profile)
        
        return step_iterator
        
    
    def get_inplace_step_iterator(self, state, step_profile):
        raise NotImplementedError('Inplace steps are not yet '
                                  'supported. They will probably become '
                                  'available in GarlicSim 0.7 in mid-2011.')
        step_function = step_profile.step_function
        step_type = get_step_type(step_function)
        
        if step_type not in (step_types.InplaceStep,
                             step_types.InplaceStepGenerator):

            raise GarlicSimException("Can't get inplace step iterator for "
                                     "`%s`, which is a non-inplace step "
                                     "function." % step_function)
            
        inplace_step_iterator_class = step_type.inplace_step_iterator_class

        inplace_step_iterator = inplace_step_iterator_class(
            state_or_history_browser,
            step_profile
        )
        
        return inplace_step_iterator
    

    def build_step_profile(self, *args, **kwargs):
        return garlicsim.misc.StepProfile.build_with_default_step_function(
            self.default_step_function,
            *args,
            **kwargs
        )

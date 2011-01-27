# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `SimpackGrokker` class.

See its documentation for more details.
'''

import types

from garlicsim.general_misc import import_tools
from garlicsim.general_misc import misc_tools
from garlicsim.general_misc import cute_iter_tools
from garlicsim.general_misc.reasoned_bool import ReasonedBool
from garlicsim.general_misc.nifty_collections import OrderedDict
from garlicsim.general_misc import caching

import garlicsim
from garlicsim.misc import InvalidSimpack, simpack_tools
from garlicsim.misc import step_iterators as step_iterators_module
from . import misc

from .settings import Settings
from .step_type import StepType
from . import step_types


class SimpackGrokker(object):
    '''Encapsulates a simpack and gives useful information and tools.'''
    
    __metaclass__ = caching.CachedType

    @staticmethod
    def create_from_state(state):
        '''
        Create a simpack grokker from a state object, possibly using cached.
        '''
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
            raise InvalidSimpack("The `%s` simpack defines a `State` class, "
                                 "but it's not a subclass of "
                                 "`garlicsim.data_structures.State`." % \
                                 simpack.__name__.rsplit('.')[-1])


        state_methods = dict(
            (name, value) for (name, value) in
            misc_tools.getted_vars(State).iteritems() if callable(value)
        )

        self.step_functions_by_type = dict((step_type, []) for step_type in
                                           step_types.step_types_list)
        '''dict mapping from each step type to step functions of that type.'''
        
        
        for method in state_methods.itervalues():
            step_type = StepType.get_step_type(method)
            if step_type:
                self.step_functions_by_type[step_type].append(method)
            
                
        if self.step_functions_by_type[step_types.HistoryStep] or \
           self.step_functions_by_type[step_types.HistoryStepGenerator]:
            
            self.history_dependent = True

            self.all_step_functions = (
                self.step_functions_by_type[step_types.HistoryStepGenerator] +
                self.step_functions_by_type[step_types.HistoryStep]
            )
            
            if (self.step_functions_by_type[step_types.SimpleStep] or
                self.step_functions_by_type[step_types.StepGenerator] or
                self.step_functions_by_type[step_types.InplaceStep] or
                self.step_functions_by_type[step_types.InplaceStepGenerator]):
                
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
            
            
        # (no-op assignments, just for docs:)
        
        self.history_dependent = self.history_dependent
        '''Flag saying whether the simpack looks at previous states.'''
        
        self.all_step_functions = self.all_step_functions
        '''
        All the step functions that the simpack provides, sorted by priority.
        '''
               
        if not self.all_step_functions:
            raise InvalidSimpack("The `%s` simpack has not defined any kind "
                                 "of step function." % \
                                 simpack.__name__.rsplit('.')[-1])
        
        self.default_step_function = self.all_step_functions[0]
        '''
        The default step function. Will be used if we don't specify another.
        '''
        
        
    def __init_analysis_settings(self):
        '''Analyze the simpack to produce a Settings object.'''
        # todo: consider doing this in `Settings.__init__`
        
        # We want to access the `.settings` of our simpack, but we don't know
        # if our simpack is a module or some other kind of object. So if it's a
        # module, we'll `try` to import `settings`.
        
        self.settings = Settings(self)
        
        if isinstance(self.simpack, types.ModuleType) and \
           not hasattr(self.simpack, 'settings'):
            
            # The `if` that we did here means: "If there's reason to suspect
            # that `self.simpack.settings` is a module that exists but hasn't
            # been imported yet."
            
            settings_module_name = ''.join((
                self.simpack.__name__,
                '.settings'
            ))
            
            import_tools.import_if_exists(settings_module_name,
                                          silent_fail=True)
            # This imports the `settings` submodule, if it exists, but it
            # does *not* keep a reference to it. We'll access `settings` as
            # an attribute of the simpack below.
            
        # Checking if there are original settings at all. If there aren't,
        # we're done.
        if hasattr(self.simpack, 'settings'):
            
            original_settings = getattr(self.simpack, 'settings')
            
            for setting_name in vars(self.settings).keys():
                if hasattr(original_settings, setting_name):
                    value = getattr(original_settings, setting_name)
                    setattr(self.settings, setting_name, value)
            # todo: currently throws away unrecognized attributes from the
            # simpack's settings.
                

    def __init_analysis_cruncher_types(self):
        '''Figure out which crunchers this simpack can use.'''
        
        # todo: possibly fix `CRUNCHERS` to some canonical state in `.settings`
        from garlicsim.asynchronous_crunching import crunchers, BaseCruncher
        simpack = self.simpack
        
        self.cruncher_types_availability = OrderedDict()
        '''dict mapping from cruncher type to whether it can be used.'''
        
        self.available_cruncher_types = []
        '''The cruncher types that this simpack can use.'''
        
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
                        'available cruncher type.' % \
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
                        'available cruncher type.' % \
                        (simpack.__name__.rsplit('.')[-1],
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
        Get a step iterator for crunching states of the simulation.
        
        The step profile will specify which parameters to pass to the simpack's
        step function.
        '''
        
        step_function = step_profile.step_function
        step_type = StepType.get_step_type(step_function)
        
        return step_type.step_iterator_class(state_or_history_browser,
                                             step_profile)
        
    
    def get_inplace_step_iterator(self, state, step_profile):
        '''
        Get an inplace step iterator which modifies the state in place.
        
        On every iteration of the inplace step iterator, `state` will be
        changed to be the next moment in the simulation. No new state objects
        will be created.
        
        This can only be used with inplace step functions.
        '''
        
        step_function = step_profile.step_function
        step_type = StepType.get_step_type(step_function)
        
        if step_type not in (step_types.InplaceStep,
                             step_types.InplaceStepGenerator):
            raise Exception("Can't get an inplace step iterator for the step "
                            "function you're using, because it's not an "
                            "inplace step function, it's a %s." % 
                            step_type.verbose_name)
        
        return step_type.inplace_step_iterator_class(
            state,
            step_profile
        )
    
    
    def is_inplace_iterator_available(self, step_profile):
        '''
        Return whether `step_profile` allows using an inplace step iterator.
        
        Only step profiles that use an inplace step function (or generator)
        allow using inplace step iterators.
        '''
        step_function = step_profile.step_function
        step_type = StepType.get_step_type(step_function)
        
        return (step_type in (step_types.InplaceStep,
                              step_types.InplaceStepGenerator))
        
    

    def build_step_profile(self, *args, **kwargs):
        '''
        Build a step profile smartly.
        
        The canonical way to build a step profile is to provide it with a step
        function, `*args` and `**kwargs`. But in this function we're being a
        little smarter so the user will have less work.
        
        You do not need to enter a step function; We will use the default one,
        unless you specify a different one as `step_function`.
        
        You may also pass in a step profile as `step_profile`, and it will be
        noticed and used.
        '''
        parse_arguments_to_step_profile = \
            garlicsim.misc.StepProfile.build_parser(
                self.default_step_function
            )
        
        step_profile = parse_arguments_to_step_profile(*args, **kwargs)
        return step_profile

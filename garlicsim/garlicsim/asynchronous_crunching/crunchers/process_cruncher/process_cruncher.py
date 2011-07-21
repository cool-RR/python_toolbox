# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `ProcessCruncher` class.

See its documentation for more information.
'''

import sys

from garlicsim.general_misc.reasoned_bool import ReasonedBool
from garlicsim.general_misc import string_tools
from garlicsim.general_misc import import_tools

import garlicsim
from garlicsim.asynchronous_crunching import BaseCruncher


multiprocessing_missing_text = (
    "`ProcessCruncher` can't be used because the "
    "`multiprocessing` module isn't installed.%s" % (
        (
            " You may find a backport of it for Python 2.5 here: "
            "http://pypi.python.org/pypi/multiprocessing"
        ) if sys.version_info[:2] <= (2, 5) else ''
    )
)

        
class ProcessCruncher(BaseCruncher):
    '''
    Cruncher that crunches from a process.
    
    A cruncher is a worker which crunches the simulation. It receives a state
    from the main program, and then it repeatedly applies the step function of
    the simulation to produce more states. Those states are then put in the
    cruncher's `.work_queue`. They are then taken by the main program when
    `Project.sync_crunchers` is called, and put into the tree.
        
    Read more about crunchers in the documentation of the `crunchers` package.
    
    The advantage of `ProcessCruncher` over `ThreadCruncher` is that
    `ProcessCruncher` is able to run on a different core of the processor in
    the machine, thus using the full power of the processor.
    '''
    
    gui_explanation = string_tools.docstring_trim(
    '''
    `ProcessCruncher`:
    
     - Works from a `multiprocessing.Process`.
    
     - Able to run on a different core of the processor than the main process 
       or other ProcessCrunchers, thus utilizing the full power of the
       processor.
     '''
    )
    
    
    def __init__(self, crunching_manager, initial_state, crunching_profile):
        
        BaseCruncher.__init__(self, crunching_manager, initial_state, 
                              crunching_profile)
        
        if not import_tools.exists('multiprocessing'):
            raise Exception(multiprocessing_missing_text)
        
        from .process import Process
        
        self.process = Process(
            self.project.simpack_grokker.get_step_iterator,
            initial_state,
            crunching_profile
        )
        '''The actual process which does the crunching.'''
        
        self.work_queue = self.process.work_queue
        '''
        Queue for putting completed work to be picked up by the main thread.
        
        In this queue the cruncher will put the states that it produces, in
        chronological order. If the cruncher reaches a simulation ends, it will
        put an `EndMarker` in this queue.
        '''
        
        self.order_queue = self.process.order_queue
        '''Queue for receiving instructions from the main thread.'''
     
    
    @staticmethod
    def can_be_used_with_simpack_grokker(simpack_grokker):
        '''
        Return whether `ProcessCruncher` can be used with `simpack_grokker`.
        
        For `ProcessCruncher` to be usable, the `multiprocessing` module must
        be installed. Assuming it's installed, `ProcessCruncher` can be used if
        and only if the simpack is not history-dependent.
        '''
        
        if not import_tools.exists('multiprocessing'):
            return ReasonedBool(
                False,
                multiprocessing_missing_text
            )
        
        elif simpack_grokker.history_dependent:
            return ReasonedBool(
                False,
                "`ProcessCruncher` can't be used in history-dependent "
                "simulations because processes don't share memory."
            )
        
        else:
            return True

        
    def start(self):
        '''
        Start the cruncher so it will start crunching and delivering states.
        '''
        self.process.start()

            
    def retire(self):
        '''
        Retire the cruncher. Process-safe.
        
        Causes it to shut down as soon as it receives the order.
        '''
        self.order_queue.put('retire')
        
        
    def update_crunching_profile(self, profile):
        '''Update the cruncher's crunching profile. Process-safe.'''
        self.order_queue.put(profile)
        
        
    def is_alive(self):
        '''Report whether the cruncher is alive and crunching.'''
        return self.process.is_alive()
        
        
    
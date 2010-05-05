# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines an EmitterSystem, which offers some benefits over Emitter.

See documentation of EmitterSystem for more info.
'''

from __future__ import with_statement

import itertools
from garlicsim.general_misc import cute_iter_tools

from emitter import Emitter


class FreezeCacheRebuildingContextManager(object):
    '''
    Context manager for freezing the cache rebuilding in an emitter system.
    
    When you do actions using this context manager, the emitters will not
    rebuild their cache when changing their inputs/outputs. When the outermost
    context manager has exited, all the caches for these emitters will get
    rebuilt.
    '''    
    def __init__(self, emitter_system):
        self.emitter_system = emitter_system
        
    def __enter__(self):
        assert self.emitter_system._cache_rebuilding_frozen >= 0
        self.emitter_system._cache_rebuilding_frozen += 1
        
    def __exit__(self, *args, **kwargs):
        self.emitter_system._cache_rebuilding_frozen -= 1
        if self.emitter_system._cache_rebuilding_frozen == 0:
            self.emitter_system._recalculate_all_cache()

            
class EmitterSystem(object):
    '''
    A system of emitters, representing a set of possible events in a program
    
    EmitterSystem offers a few advantages over using plain emitters.
    
    There are the `bottom_emitter` and `top_emitter`, which allow, respectively,
    to keep track of each `emit`ting that goes on, and to generate an `emit`ting
    that affects all emitters in the system.
    
    The EmitterSystem also offers a context manager, `.freeze_cache_rebuilding`.
    When you do actions using this context manager, the emitters will not
    rebuild their cache when changing their inputs/outputs. When the outermost
    context manager has exited, all the caches for these emitters will get
    rebuilt.
    '''
    # possible future idea: there is the idea of optimizing by cutting redundant
    # links between boxes. I'm a bit suspicious of it. The next logical step is
    # to make inputs and outputs abstract.
    def __init__(self):
        
        self._cache_rebuilding_frozen = 0
        self.freeze_cache_rebuilding = \
            FreezeCacheRebuildingContextManager(self)
        
        self.emitters = set()
        
        self.bottom_emitter = Emitter(self, name='bottom')
        self.emitters.add(self.bottom_emitter)
        
        self.top_emitter = Emitter(
            self,
            outputs=(self.bottom_emitter,),
            name='top',
        )
        self.emitters.add(self.top_emitter)
        
            
    def make_emitter(self, inputs=(), outputs=(), name=None):
        '''Create an emitter in this emitter system. Returns the emitter.'''

        # todo: allow one value in inputs and outputs. do in all emitter
        # constructors.
        
        inputs = set(inputs)
        inputs.add(self.top_emitter)
        outputs = set(outputs)
        outputs.add(self.bottom_emitter)
        emitter = Emitter(self, inputs, outputs, name)
        self.emitters.add(emitter)
        return emitter
    
    def remove_emitter(self, emitter):
        '''
        Remove an emitter from this system, disconnecting it from everything.
        '''
        with self.freeze_cache_rebuilding:
            emitter.disconnect_from_all()
        self.emitters.remove(emitter)
        
    def _recalculate_all_cache(self):
        '''Recalculate the cache for all the emitters.'''
        self.bottom_emitter._recalculate_total_callable_outputs_recursively()
    


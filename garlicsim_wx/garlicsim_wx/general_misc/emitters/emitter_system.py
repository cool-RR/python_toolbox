import itertools
from garlicsim.general_misc import cute_iter_tools

from .emitter import Emitter

class EmitterSystemEmitter(Emitter):    
    def __init__(self, emitter_system, inputs=(), outputs=(), name=None):
        self.emitter_system = emitter_system
        Emitter.__init__(self, inputs=inputs, outputs=outputs, name=name)        
                        
    def _recalculate_total_callable_outputs_recursively(self):
        if self.emitter_system._cache_rebuilding_frozen == 0:
            Emitter._recalculate_total_callable_outputs_recursively(self)
        
    def add_input(self, emitter):
        assert emitter in self.emitter_system.emitters
        Emitter.add_input(self, emitter)
    
    def add_output(self, thing):
        if isinstance(thing, Emitter):
            assert thing in self.emitter_system.emitters
        Emitter.add_output(self, thing)
    

class FreezeCacheRebuildingContextManager(object):
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
    # possible future idea: there is the idea of optimizing by cutting redundant
    # links between boxes. I'm a bit suspicious of it. The next logical step is
    # to make inputs and outputs abstract.
    def __init__(self):
        
        self._cache_rebuilding_frozen = 0
        self.freeze_cache_rebuilding = \
            FreezeCacheRebuildingContextManager(self)
        
        self.emitters = set()
        
        self.bottom_emitter = EmitterSystemEmitter(self)
        self.emitters.add(self.bottom_emitter)
        
        self.top_emitter = EmitterSystemEmitter(
            self,
            outputs=(self.bottom_emitter,)
        )
        self.emitters.add(self.top_emitter)
        
            
    def make_emitter(self, inputs=(), outputs=(), name=None):

        inputs = set(inputs)
        inputs.add(self.top_emitter)
        outputs = set(outputs)
        outputs.add(self.bottom_emitter)
        emitter = EmitterSystemEmitter(self, inputs, outputs, name)
        self.emitters.add(emitter)
        return emitter
    
    def remove_emitter(self, emitter):
        with self.freeze_cache_rebuilding:
            emitter.disconnect_from_all()
        self.emitters.remove(emitter)
        
    def _recalculate_all_cache(self):
        self.bottom_emitter._recalculate_total_callable_outputs_recursively()
    


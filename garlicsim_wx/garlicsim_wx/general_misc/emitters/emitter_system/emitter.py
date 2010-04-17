from ..emitter import Emitter as OriginalEmitter

class Emitter(OriginalEmitter):
    def __init__(self, emitter_system, inputs=(), outputs=(), name=None):
        self.emitter_system = emitter_system
        OriginalEmitter.__init__(self, inputs=inputs, outputs=outputs, name=name)        
                        
    def _recalculate_total_callable_outputs_recursively(self):
        if self.emitter_system._cache_rebuilding_frozen == 0:
            OriginalEmitter._recalculate_total_callable_outputs_recursively(self)
        
    def add_input(self, emitter):
        assert emitter in self.emitter_system.emitters
        OriginalEmitter.add_input(self, emitter)
    
    def add_output(self, thing):
        if isinstance(thing, Emitter):
            assert thing in self.emitter_system.emitters
        OriginalEmitter.add_output(self, thing)

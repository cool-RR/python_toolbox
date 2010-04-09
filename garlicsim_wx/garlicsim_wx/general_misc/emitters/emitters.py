
import itertools
from garlicsim.general_misc import cute_iter_tools

class EmitterSystem(object):
    #todo later: optimize by cutting redundant links between boxes
    def __init__(self):
        self.bottom_emitter = Emitter()
        self.top_emitter = Emitter(outputs=(self.bottom_emitter,))
        self.emitters = set()
    
    def make_emitter(self, inputs=(), outputs=()):
        assert cute_iter_tools.is_iterable(inputs) and \
               cute_iter_tools.is_iterable(outputs)
        inputs = set(inputs)
        inputs.add(self.top_emitter)
        outputs = set(outputs)
        outputs.add(self.bottom_emitter)
        emitter = Emitter(inputs, outputs)
        self.emitters.add(emitter)
        return emitter
    
    def remove_emitter(self, emitter):
        emitter.disconnect_from_all()
        self.emitters.remove(emitter)
        

class Emitter(object):
    
    # todo: can make "freeze_cache_rebuilding" context manager. how used with
    # multiple events?
    def __init__(self, inputs=(), outputs=()):
        self.inputs = set()
        self.outputs = set()        
        for input in inputs:
            self.add_input(input)
        for output in outputs:
            self.add_output(output)
        self._recalculate_total_callable_outputs()
   
    def _get_input_layers(self):

        input_layers = [self.inputs]
        current_input_layer = self.inputs
        while True:
            next_layer = reduce(
                set.union,
                (input.inputs for input in current_input_layer),
                set()
            )
                
        
    def _recalculate_total_callable_outputs(self):
        for input in self.inputs
        children_callable_outputs = reduce(
            set.union,
            (emitter.get_total_callable_outputs() for emitter
             in self.get_emitter_outputs() if emitter is not self),
            set()
        )
        
        self.__total_callable_outputs_cache = \
            children_callable_outputs.union(self.get_callable_outputs())
    
    def get_total_inputs(self):
        
        total_inputs_of_inputs = reduce(
            set.union,
            (emitter._get_total_inputs() for emitter
             in self.inputs if emitter is not self),
            set()
        )
        
        return total_inputs_of_inputs.union(self.inputs)

    def add_input(self, emitter):
        assert isinstance(emitter, Emitter)
        self.inputs.add(emitter)
        emitter.outputs.add(self)
        
    def remove_input(self, emitter):
        assert isinstance(emitter, Emitter)
        self.inputs.remove(emitter)
        emitter.outputs.remove(self)
    
    def add_output(self, thing):
        assert isinstance(thing, Emitter) or callable(thing)
        self.outputs.add(thing)
        if isinstance(thing, Emitter):
            thing.inputs.add(self)
        
    def remove_output(self, thing):
        assert isinstance(thing, Emitter) or callable(thing)
        self.outputs.remove(thing)
        emitter.inputs.remove(self)
        
    def disconnect_from_all(self):
        for input in self.inputs:
            self.remove_input(input)
        for output in self.outputs:
            self.remove_output(output)
        
    def get_callable_outputs(self):
        return set((
            output for output in self.outputs if callable(output)
        ))
    
    def get_emitter_outputs(self):
        return set((
            output for output in self.outputs if isinstance(output, Emitter)
        ))
        
    def get_total_callable_outputs(self):
        return self.__total_callable_outputs_cache
    
    def emit(self):
        # Note that this function gets called many times, so it should be
        # optimized for speed.
        for callable_output in self.__total_callable_outputs_cache:
            # We are using the cache directly instead of calling the getter, for
            # speed.
            callable_output()

import itertools
from garlicsim.general_misc import cute_iter_tools

class EmitterSystem(object):
    #todo later: optimize by cutting redundant links between boxes
    def __init__(self):
        self.bottom_emitter = Emitter()
        self.top_emitter = Emitter(outputs=(self.bottom_emitter,))
        self.emitters = set()
    
    def make_emitter(self, inputs=(), outputs=()):
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
    def __init__(self, inputs=(), outputs=()):
        self.inputs = set()
        self.outputs = set()
        for input in inputs:
            self.add_input(input)
        for output in outputs:
            self.add_output(output)
            
    
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
        
    def get_total_callable_outputs(self): # rename "total"
        
        children_callable_outputs = reduce(
            set.union,
            (emitter.get_total_callable_outputs() for emitter
             in self.get_emitter_outputs() if emitter is not self),
            set()
        )
        
        return children_callable_outputs.union(self.get_callable_outputs())
    
    def emit(self):
        # print self # debug
        for callable_output in self.get_total_callable_outputs():
            callable_output()

import itertools
from garlicsim.general_misc import cute_iter_tools

# todo: there should probably some circularity check. Maybe actually circularity
# should be permitted?

        
        
class Emitter(object):
    
    
    def __init__(self, inputs=(), outputs=(), name=None):

        assert cute_iter_tools.is_iterable(inputs) and \
               cute_iter_tools.is_iterable(outputs)
        
        self._inputs = set()
        self._outputs = set()
        
        for output in outputs:
            self.add_output(output)
            
        self._recalculate_total_callable_outputs()        

        # We made sure to create the callable outputs cache before we add
        # inputs, so when we update their cache, it could use ours.
        for input in inputs:
            self.add_input(input)

        self.name = name
        #if name:
            #self.name = name
        #else:
            #try:
                #self.name = \
                    #magic_tools.get_name_of_attribute_that_we_will_become()
            #except Exception:
                #self.name = None

    def get_inputs(self):
        return self._inputs
    
    def get_outputs(self):
        return self._outputs
                
    def _get_input_layers(self):

        input_layers = [self._inputs]
        current_layer = self._inputs
        while current_layer:
            
            next_layer = reduce(
                set.union,
                (input._inputs for input in current_layer),
                set()
            )
            
            for ancestor_layer in input_layers:
                assert isinstance(next_layer, set)
                next_layer -= ancestor_layer

            input_layers.append(next_layer)
            
            current_layer = next_layer        

        # todo: remove this assert:
        assert sum(len(layer) for layer in input_layers) == \
               len(reduce(set.union, input_layers, set()))
            
        return input_layers
                
        
    def _recalculate_total_callable_outputs_recursively(self):
        
        # todo: I suspect this wouldn't work for the following case. `self` has
        # inputs `A` and `B`. `A` has input `B`. A callable output `func` was
        # just removed from `self`, so this function got called. We update the
        # cache here, then take the first input layer, which is `A` and `B` in
        # some order. Say `B` is first. Now, we do `recalculate` on `B`, but `A`
        # still got the cache with `func`, and `B` will take that. I need to
        # test this.
        # 
        # I have an idea how to solve it: In the getter of the cache, check the
        # cache exists, otherwise rebuild. The reason we didn't do it up to now
        # was to optimize for speed, but only `emit` needs to be fast and it
        # doesn't use the getter. We'll clear the caches of all inputs, and
        # they'll rebuild as they call each other.
        
        self._recalculate_total_callable_outputs()
        input_layers = self._get_input_layers()
        for input_layer in input_layers:
            for input in input_layer:
                input._recalculate_total_callable_outputs()
        
        
    def _recalculate_total_callable_outputs(self):
        children_callable_outputs = reduce(
            set.union,
            (emitter.get_total_callable_outputs() for emitter
             in self._get_emitter_outputs() if emitter is not self),
            set()
        )
        
        self.__total_callable_outputs_cache = \
            children_callable_outputs.union(self._get_callable_outputs())

    def add_input(self, emitter):
        assert isinstance(emitter, Emitter)
        self._inputs.add(emitter)
        emitter._outputs.add(self)
        emitter._recalculate_total_callable_outputs_recursively()
        
    def remove_input(self, emitter):
        assert isinstance(emitter, Emitter)
        self._inputs.remove(emitter)
        emitter._outputs.remove(self)
        emitter._recalculate_total_callable_outputs_recursively()
    
    def add_output(self, thing):
        assert isinstance(thing, Emitter) or callable(thing)
        self._outputs.add(thing)
        if isinstance(thing, Emitter):
            thing._inputs.add(self)
        self._recalculate_total_callable_outputs_recursively()
        
    def remove_output(self, thing):
        assert isinstance(thing, Emitter) or callable(thing)
        self._outputs.remove(thing)
        emitter._inputs.remove(self)
        self._recalculate_total_callable_outputs_recursively()
        
    def disconnect_from_all(self): # todo: use the freeze here
        for input in self._inputs: 
            self.remove_input(input)
        for output in self._outputs:
            self.remove_output(output)
        
    def _get_callable_outputs(self):
        return set((
            output for output in self._outputs if callable(output)
        ))
    
    def _get_emitter_outputs(self):
        return set((
            output for output in self._outputs if isinstance(output, Emitter)
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
    
    def __repr__(self):
        return '<%s.%s %sat %s>' % (
            self.__class__.__module__,
            self.__class__.__name__,
            ''.join(("'", self.name, "' ")) if self.name else '',
            hex(id(self))
        )
    """
    Unused:
    
    def _get_total_inputs(self):
        
        total_inputs_of_inputs = reduce(
            set.union,
            (emitter._get_total_inputs() for emitter
             in self._inputs if emitter is not self),
            set()
        )
        
        return total_inputs_of_inputs.union(self._inputs)
    """
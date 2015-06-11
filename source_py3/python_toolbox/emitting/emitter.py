# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''
Defines the `Emitter` class.

See its documentation for more info.
'''

# todo: there should probably be some circularity check. Maybe actually
# circularity should be permitted?

# todo: make some way to emit from multiple emitters simulataneously, saving
# redundant calls to shared callable outputs.

import itertools
import collections
import functools

from python_toolbox import cute_iter_tools
from python_toolbox import misc_tools
from python_toolbox import address_tools
        

class Emitter:
    '''
    An emitter you can `emit` from to call all its callable outputs.
    
    The emitter idea is a variation on the publisher-subscriber design pattern.

    Every emitter has a set of inputs and a set of outputs. The inputs, if
    there are any, must be emitters themselves. So when you `emit` on any of
    this emitter's inputs, it's as if you `emit`ted on this emitter as well.
    (Recursively, of course.)
    
    The outputs are a bit different. An emitter can have as outputs both (a)
    other emitters and (b) callable objects. (Which means, functions or
    function-like objects.)
    
    There's no need to explain (a): If `emitter_1` has as an output
    `emitter_2`, then `emitter_2` has as an input `emitter_1`, which works like
    how we explained above about inputs.
    
    But now (b): An emitter can have callables as outputs. (Without these, the
    emitter idea won't have much use.) These callables simply get called
    whenever the emitter or one of its inputs get `emit`ted.
    
    The callables that you register as outputs are functions that need to be
    called when the original event that caused the `emit` action happens.
    '''
    
    _is_atomically_pickleable = False

    
    def __init__(self, inputs=(), outputs=(), name=None):
        '''
        Construct the emitter.
        
        `inputs` is an iterable of inputs, all of which must be emitters. (You
        can also pass in a single input without using an iterable.)
        
        `outputs` is an iterable of outputs, which may be either emitters or
        callables. (You can also pass in a single output without using an
        iterable.)
        
        `name` is a string name for the emitter. (Optional, helps with
        debugging.)
        '''
        
        from python_toolbox import sequence_tools

        inputs = sequence_tools.to_tuple(inputs,
                                         item_type=Emitter)
        outputs = sequence_tools.to_tuple(outputs,
                                          item_type=(collections.Callable,
                                                     Emitter))
        
        self._inputs = set()
        '''The emitter's inputs.'''
        
        self._outputs = set()
        '''The emitter's inputs.'''
        
        for output in outputs:
            self.add_output(output)
                        
        self.__total_callable_outputs_cache = None
        '''
        A cache of total callable outputs.
        
        This means the callable outputs of this emitter and any output
        emitters.
        '''
        
        self._recalculate_total_callable_outputs()        

        # We made sure to create the callable outputs cache before we add
        # inputs, so when we update their cache, it could use ours.
        for input in inputs:
            self.add_input(input)

        self.name = name
        '''The emitter's name.'''

    def get_inputs(self):
        '''Get the emitter's inputs.'''
        return self._inputs
    
    def get_outputs(self):
        '''Get the emitter's outputs.'''
        return self._outputs
                
    def _get_input_layers(self):
        '''
        Get the emitter's inputs as a list of layers.
        
        Every item in the list will be a list of emitters on that layer. For
        example, the first item will be a list of direct inputs of our emitter.
        The second item will be a list of *their* inputs. Etc.
        
        Every emitter can appear only once in this scheme: It would appear on
        the closest layer that it's on.
        '''

        input_layers = [self._inputs]
        current_layer = self._inputs
        while current_layer:
            
            next_layer = functools.reduce(
                set.union,
                (input._inputs for input in current_layer),
                set()
            )
            
            for ancestor_layer in input_layers:
                assert isinstance(next_layer, set)
                next_layer -= ancestor_layer

            input_layers.append(next_layer)
            
            current_layer = next_layer        

        
        # assert sum(len(layer) for layer in input_layers) == \
        #        len(reduce(set.union, input_layers, set()))
            
        return input_layers
                
        
    def _recalculate_total_callable_outputs_recursively(self):
        '''
        Recalculate `__total_callable_outputs_cache` recursively.
        
        This will to do the recalculation for this emitter and all its inputs.
        '''
        
        # todo: I suspect this wouldn't work for the following case. `self` has
        # inputs `A` and `B`. `A` has input `B`. A callable output `func` was
        # just removed from `self`, so this function got called. We update the
        # cache here, then take the first input layer, which is `A` and `B` in
        # some order. Say `B` is first. Now, we do `recalculate` on `B`, but
        # `A` still got the cache with `func`, and `B` will take that. I need
        # to test this.
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
        '''
        Recalculate `__total_callable_outputs_cache` for this emitter.
        
        This will to do the recalculation for this emitter and all its inputs.
        '''
        children_callable_outputs = functools.reduce(
            set.union,
            (emitter.get_total_callable_outputs() for emitter
             in self._get_emitter_outputs() if emitter is not self),
            set()
        )
        
        self.__total_callable_outputs_cache = \
            children_callable_outputs.union(self._get_callable_outputs())

    def add_input(self, emitter):
        '''
        Add an emitter as an input to this emitter.

        Every time that emitter will emit, it will cause this emitter to emit
        as well.
        '''
        assert isinstance(emitter, Emitter)
        self._inputs.add(emitter)
        emitter._outputs.add(self)
        emitter._recalculate_total_callable_outputs_recursively()
        
    def remove_input(self, emitter):
        '''Remove an input from this emitter.'''
        assert isinstance(emitter, Emitter)
        self._inputs.remove(emitter)
        emitter._outputs.remove(self)
        emitter._recalculate_total_callable_outputs_recursively()
    
    def add_output(self, thing):
        '''
        Add an emitter or a callable as an output to this emitter.
        
        If adding a callable, every time this emitter will emit the callable
        will be called.
        
        If adding an emitter, every time this emitter will emit the output
        emitter will emit as well.
        '''
        assert isinstance(thing, (Emitter, collections.Callable))
        self._outputs.add(thing)
        if isinstance(thing, Emitter):
            thing._inputs.add(self)
        self._recalculate_total_callable_outputs_recursively()
        
    def remove_output(self, thing):
        '''Remove an output from this emitter.'''
        assert isinstance(thing, (Emitter, collections.Callable))
        self._outputs.remove(thing)
        if isinstance(thing, Emitter):
            thing._inputs.remove(self)
        self._recalculate_total_callable_outputs_recursively()
        
    def disconnect_from_all(self): # todo: use the freeze here
        '''Disconnect the emitter from all its inputs and outputs.'''
        for input in self._inputs: 
            self.remove_input(input)
        for output in self._outputs:
            self.remove_output(output)
        
    def _get_callable_outputs(self):
        '''Get the direct callable outputs of this emitter.'''
        return set(filter(callable, self._outputs))
    
    def _get_emitter_outputs(self):
        '''Get the direct emitter outputs of this emitter.'''
        return {output for output in self._outputs if isinstance(output, Emitter)}
        
    def get_total_callable_outputs(self):
        '''
        Get the total of callable outputs of this emitter.
        
        This means the direct callable outputs, and the callable outputs of
        emitter outputs.
        '''
        return self.__total_callable_outputs_cache
    
    def emit(self):
        '''
        Call all of the (direct or indirect) callable outputs of this emitter.
        
        This is the most important method of the emitter. When you `emit`, all
        the callable outputs get called in succession.
        '''
        # Note that this function gets called many times, so it should be
        # optimized for speed.
        for callable_output in self.__total_callable_outputs_cache:
            # We are using the cache directly instead of calling the getter,
            # for speed.
            callable_output()
    
    def __repr__(self):
        '''
        Get a string representation of the emitter.
        
        Example output:        
        <python_toolbox.emitting.emitter.Emitter 'tree_modified' at
        0x1c013d0>
        '''
        return '<%s %sat %s>' % (
            address_tools.describe(type(self), shorten=True),
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
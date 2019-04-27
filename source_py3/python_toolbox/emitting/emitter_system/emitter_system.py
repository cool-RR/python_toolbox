# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''
Defines an EmitterSystem, which offers some benefits over Emitter.

See documentation of EmitterSystem for more info.
'''


import itertools

from python_toolbox import freezing
from python_toolbox import cute_iter_tools

from .emitter import Emitter


class EmitterSystem:
    '''
    A system of emitters, representing a set of possible events in a program.

    `EmitterSystem` offers a few advantages over using plain emitters.

    There are the `bottom_emitter` and `top_emitter`, which allow,
    respectively, to keep track of each `emit`ting that goes on, and to
    generate an `emit`ting that affects all emitters in the system.

    The `EmitterSystem` also offers a context manager,
    `.freeze_cache_rebuilding`. When you do actions using this context manager,
    the emitters will not rebuild their cache when changing their
    inputs/outputs. When the outermost context manager has exited, all the
    caches for these emitters will get rebuilt.
    '''
    # possible future idea: there is the idea of optimizing by cutting
    # redundant links between boxes. I'm a bit suspicious of it. The next
    # logical step is to make inputs and outputs abstract.
    def __init__(self):

        self.emitters = set()

        self.bottom_emitter = Emitter(self, name='bottom')
        self.emitters.add(self.bottom_emitter)

        self.top_emitter = Emitter(
            self,
            outputs=(self.bottom_emitter,),
            name='top',
        )
        self.emitters.add(self.top_emitter)


    cache_rebuilding_freezer = freezing.FreezerProperty()
    '''
    Context manager for freezing the cache rebuilding in an emitter system.

    When you do actions using this context manager, the emitters will not
    rebuild their cache when changing their inputs/outputs. When the outermost
    context manager has exited, all the caches for these emitters will get
    rebuilt.
    '''


    @cache_rebuilding_freezer.on_thaw
    def _recalculate_all_cache(self):
        '''Recalculate the cache for all the emitters.'''
        self.bottom_emitter._recalculate_total_callable_outputs_recursively()



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
        with self.cache_rebuilding_freezer:
            emitter.disconnect_from_all()
        self.emitters.remove(emitter)






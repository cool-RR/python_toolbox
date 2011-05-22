# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `` class.

See its documentation for more information.
'''

from garlicsim.general_misc.freezers import FreezerProperty, Freezer
from garlicsim.general_misc import caching


class CustomFreezer(Freezer):
    ''' '''
    def __init__(self, obj):
        self.obj = obj
        
    def freeze_handler(obj):
        self.objdifferent_type_freeze_counter += 1
        
    def thaw_handler(obj):
        self.objdifferent_type_thaw_counter += 1

        
def test():
    class A(object):

        
        
        lone_freezer = FreezerProperty()
        
        ### Defining decorate-happy freezer: ##################################
        #                                                                     #
        decorate_happy_freeze_counter = caching.CachedProperty(lambda self: 0)
        decorate_happy_thaw_counter = caching.CachedProperty(lambda self: 0)
        decorate_happy_freezer = FreezerProperty()
        @decorate_happy_freezer.on_freeze
        def increment_decorate_happy_freeze_counter(self):
            self.decorate_happy_freeze_counter += 1
        @decorate_happy_freezer.on_thaw
        def increment_decorate_happy_thaw_counter(self):
            self.decorate_happy_thaw_counter += 1
        #                                                                     #
        ### Finished defining decorate-happy freezer. #########################
        
        ### Defining argument-happy freezer: ##################################
        #                                                                     #
        argument_happy_freeze_counter = caching.CachedProperty(lambda self: 0)
        argument_happy_thaw_counter = caching.CachedProperty(lambda self: 0)        
        def increment_argument_happy_freeze_counter(self):
            self.argument_happy_freeze_counter += 1
        def increment_argument_happy_thaw_counter(self):
            self.argument_happy_thaw_counter += 1
        argument_happy_freezer = FreezerProperty(
            on_freeze=increment_argument_happy_freeze_counter,
            on_thaw=increment_argument_happy_thaw_counter
        )
        #                                                                     #
        ### Finished defining argument-happy freezer. #########################
        
        ### Defining mixed freezer: ###########################################
        #                                                                     #
        mix_freeze_counter = caching.CachedProperty(lambda self: 0)
        mix_thaw_counter = caching.CachedProperty(lambda self: 0)
        def increment_mix_freeze_counter(self):
            self.mix_freeze_counter += 1
        mix_freezer = FreezerProperty(on_freeze=increment_mix_freeze_counter)
        @mix_freezer.on_thaw
        def increment_mix_thaw_counter(self):
            self.mix_thaw_counter += 1
        #                                                                     #
        ### Finished defining mixed freezer. ##################################
        
        ### Defining freezer with different freezer type: #####################
        #                                                                     #
        different_type_freeze_counter = caching.CachedProperty(lambda self: 0)
        different_type_thaw_counter = caching.CachedProperty(lambda self: 0)
        different_type_freezer = FreezerProperty(on_freeze=increment_different_type_freeze_counter)
        @different_type_freezer.on_thaw
        def increment_different_type_thaw_counter(self):
            self.different_type_thaw_counter += 1
        #                                                                     #
        ### Finished defining freezer with different freezer type. ############

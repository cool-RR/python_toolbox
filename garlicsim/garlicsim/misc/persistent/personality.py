# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the Personality class.

See its documentation for more information.
'''

from persistent import Persistent

class Personality(object):
    '''
    A bunch of easy-to-remember attributes associated with a persistent object.
    
    These attributes include:
      * A human name
      * A light color
      * A dark color
    
    Each persistent object has a personality associated with it, generated
    automatically from its uuid. The personality makes it easy for humans to
    identify the persistent object.
    
    Colors are specified in HSL.
    '''
    
    def __init__(self, persistent):

        assert isinstance(persistent, Persistent)
        
        import human_names

        color_resolution = 100
        
        u = int(persistent._Persistent__uuid)
        
        (u, human_name_seed) = divmod(u, 5494)
        self.human_name = human_names.name_list[human_name_seed]
        
        color_seeds = []
        for i in range(4):
            (u, new_color_seed) = divmod(u, color_resolution)
            color_seeds.append(new_color_seed)
        

        normalized_color_seeds = \
            [color_seed * (1.0/color_resolution) for color_seed in color_seeds]
        
        self.light_color = normalized_color_seeds[0:2] + [0.9]
        self.dark_color = normalized_color_seeds[2:4] + [0.1]
        
                          
                        
                          

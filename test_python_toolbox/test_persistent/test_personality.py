# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `python_toolbox.persistent.personality.Personality`.'''

import colorsys

from python_toolbox.persistent import CrossProcessPersistent


def test():
    '''Test the basic workings of `Personality`.'''
    cpp_1 = CrossProcessPersistent()
    cpp_2 = CrossProcessPersistent()
    cpp_3 = CrossProcessPersistent()
    
    personality_1 = cpp_1.personality
    personality_2 = cpp_2.personality
    personality_3 = cpp_3.personality
    
    human_name_1 = personality_1.human_name
    human_name_2 = personality_2.human_name
    human_name_3 = personality_3.human_name
    
    assert isinstance(human_name_1, basestring)
    assert isinstance(human_name_2, basestring)
    assert isinstance(human_name_3, basestring)
    
    light_color_1 = personality_1.light_color
    light_color_2 = personality_2.light_color
    light_color_3 = personality_3.light_color
    dark_color_1 = personality_1.dark_color
    dark_color_2 = personality_2.dark_color
    dark_color_3 = personality_3.dark_color
    
    for light_color in (light_color_1, light_color_2, light_color_3):
        hls_value = colorsys.rgb_to_hls(*light_color)
        lightness = hls_value[1]
        assert 0.85 < lightness < 0.95
        
    for dark_color in (dark_color_1, dark_color_2, dark_color_3):
        hls_value = colorsys.rgb_to_hls(*dark_color)
        lightness = hls_value[1]
        assert 0.25 < lightness < 0.35
    
    assert (human_name_1, light_color_1, dark_color_1) != \
           (human_name_2, light_color_2, dark_color_2) != \
           (human_name_3, light_color_3, dark_color_3) != \
           (human_name_1, light_color_1, dark_color_1)
    
    
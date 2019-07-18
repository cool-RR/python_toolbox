# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import color_tools

def test():
    ''' '''
    assert color_tools.mix_rgb(0.5, (0, 1, 0.5), (1, 0, 0)) == (0.5, 0.5, 0.25)
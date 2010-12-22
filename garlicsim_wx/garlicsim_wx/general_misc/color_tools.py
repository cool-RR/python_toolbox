# Copyright 2009-2011 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''Defines tools for manipulating colors.'''


def mix_rgb(ratio, rgb1, rgb2):
    '''Mix two rgb colors `rgb1` and `rgb2`, according to the given `ratio`.'''
    counter_ratio = 1 - ratio
    return (
        rgb1[0] * ratio + rgb2[0] * counter_ratio,
        rgb1[1] * ratio + rgb2[1] * counter_ratio,
        rgb1[2] * ratio + rgb2[2] * counter_ratio
    )
        
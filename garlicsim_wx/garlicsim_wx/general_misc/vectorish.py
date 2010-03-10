# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
This is a terrible little module for manipulating tuples of two items as 2d
vectors.
'''

import math

def add(vec1, vec2):
    return tuple((vec1[i] + vec2[i]) for i in xrange(len(vec1)))

def mult(scal, vec1):
    return tuple(vec1[i] * scal for i in xrange(len(vec1)))

def average(vec1, vec2):
    return mult(0.5, add(vec1, vec2))

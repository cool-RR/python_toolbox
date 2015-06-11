# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines various tools for pickling and unpickling.'''


import zlib
import pickle as pickle_module

 
def compickle(thing):
    '''Pickle `thing` and compress it using `zlib`.'''
    return zlib.compress(pickle_module.dumps(thing, protocol=2))

def decompickle(thing):
    '''Unpickle `thing` after decompressing it using `zlib`.'''
    return pickle_module.loads(zlib.decompress(thing))
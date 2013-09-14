# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''Test that `cute_pickle` uses `cPickle` and not `pickle`.'''


from python_toolbox import pickle_tools

def test():
    '''Test that `cute_pickle` uses `cPickle` and not `pickle`.'''
    import cPickle
    assert pickle_tools.pickle_module is cPickle
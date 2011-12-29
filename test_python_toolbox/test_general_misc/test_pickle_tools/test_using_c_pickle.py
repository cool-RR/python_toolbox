# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Test that `cute_pickle` uses `cPickle` and not `pickle`.'''


from garlicsim.general_misc import pickle_tools

def test():
    '''Test that `cute_pickle` uses `cPickle` and not `pickle`.'''
    import cPickle
    assert pickle_tools.pickle_module is cPickle
from garlicsim.general_misc import pickle_tools

def test():
    import cPickle
    assert pickle_tools.pickle_module is cPickle
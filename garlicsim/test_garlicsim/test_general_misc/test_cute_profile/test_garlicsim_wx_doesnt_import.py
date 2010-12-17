import sys


def test_garlicsim_wx_doesnt_import():
    # Ideally we should be ensuring here that `garlicsim` isn't imported, or
    # unimporting it somehow. I don't know how to reliably do that yet, so I
    # just assume that `nose` imported only `garlicsim` without importing
    # `garlicsim.general_misc.cute_profile`.
    import garlicsim_wx
    assert 'garlicsim_wx' in sys.modules
    assert 'garlicsim' in sys.modules
    assert 'garlicsim.general_misc.cute_profile' not in sys.modules
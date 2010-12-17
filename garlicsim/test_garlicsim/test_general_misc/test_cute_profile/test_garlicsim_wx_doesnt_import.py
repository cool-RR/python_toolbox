import sys

import nose

import garlicsim


def test_garlicsim_wx_doesnt_import():
    '''
    
    It's important that `garlicsim` and `garlicsim_wx` won't import
    `cute_profile` by default since on Ubuntu the required `pstats` module isn't
    always available, and we wouldn't want to send the user to download it if he
    just wants to use `garlicsim` (or `_wx`) and the `cute_profile` module
    itself.
    '''
    # Ideally we should be ensuring here that `garlicsim` isn't imported, or
    # unimporting it somehow. I don't know how to reliably do that yet, so I
    # just assume that `nose` imported only `garlicsim` without importing
    # `garlicsim.general_misc.cute_profile`.
    
    if garlicsim.__version_info__ <= (0, 6, 0):
        raise nose.SkipTest("Don't know how to ensure nose/wing start test "
                            "with nothing imported")
    import garlicsim_wx
    assert 'garlicsim_wx' in sys.modules
    assert 'garlicsim' in sys.modules
    assert 'garlicsim.general_misc.cute_profile' not in sys.modules
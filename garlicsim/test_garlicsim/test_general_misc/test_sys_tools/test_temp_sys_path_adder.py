import sys

from garlicsim.general_misc.sys_tools import TempSysPathAdder

def test_single():
    other_path = 'afdgfasgg38gjh3908ga'
    assert other_path not in sys.path
    with TempSysPathAdder(other_path):
        assert other_path in sys.path
    assert other_path not in sys.path
    
def test_multiple():
    other_paths = ['wf43f3_4f', 'argaer\\5g_']
    for other_path in other_paths:
        assert other_path not in sys.path
    with TempSysPathAdder(other_paths):
        for other_path in other_paths:
            assert other_path in sys.path
    for other_path in other_paths:
        assert other_path not in sys.path
    
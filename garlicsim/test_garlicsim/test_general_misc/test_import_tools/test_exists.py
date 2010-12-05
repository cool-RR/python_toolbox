import nose.tools

from garlicsim.general_misc import import_tools
from garlicsim.general_misc.import_tools import exists

def test():
    assert not exists('adfgadbnv5nrn')
    assert not exists('45gse_e5b6_DFDF')
    assert not exists('VWEV65hnrt___a4')
    assert exists('email')
    assert exists('re')
    assert exists('sys')
    nose.tools.assert_raises(Exception, lambda: exists('email.encoders'))
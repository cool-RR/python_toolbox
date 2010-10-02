
import re

from garlicsim.general_misc import re_tools
from garlicsim.general_misc.re_tools import searchall


def test_search_all():
    s = 'asdf df sfg s'
    result = searchall('(\w+)', s)
    assert len(result) == 4
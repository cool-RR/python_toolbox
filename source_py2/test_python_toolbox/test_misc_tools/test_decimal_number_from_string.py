# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

import nose.tools

from python_toolbox import cute_testing

from python_toolbox.misc_tools import decimal_number_from_string


def test():
    assert decimal_number_from_string('7') == 7
    assert type(decimal_number_from_string('7')) == int
    assert decimal_number_from_string('-12.34') == -12.34
    assert type(decimal_number_from_string('-12.34')) == float
    with cute_testing.RaiseAssertor():
        decimal_number_from_string(31412)
    with cute_testing.RaiseAssertor():
        decimal_number_from_string('JJfa')
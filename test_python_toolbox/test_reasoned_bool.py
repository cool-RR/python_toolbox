# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `python_toolbox.reasoned_bool.ReasonedBool`.'''

from python_toolbox.reasoned_bool import ReasonedBool

def test():
    '''Test the basic workings of `ReasonedBool`.'''
    assert True == ReasonedBool(True)
    assert True == ReasonedBool(True, "Because I feel like it")
    assert ReasonedBool(True)
    assert ReasonedBool(True, "Because I feel like it")
    assert bool(ReasonedBool(True)) is True
    assert bool(ReasonedBool(True, "Because I feel like it")) is True

    assert False == ReasonedBool(False)
    assert False == ReasonedBool(False, "Because I don't feel like it")
    assert not ReasonedBool(False)
    assert not ReasonedBool(False, "Because I don't feel like it")
    assert bool(ReasonedBool(False)) is False
    assert bool(ReasonedBool(False, "Because I don't feel like it")) is False


    assert ReasonedBool(True, "Meow") == ReasonedBool(True, "Woof")

    assert ReasonedBool(False, "Meow") == ReasonedBool(False, "Woof")

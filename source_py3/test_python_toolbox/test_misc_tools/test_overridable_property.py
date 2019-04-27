# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import cute_testing

from python_toolbox.misc_tools import OverridableProperty


def test():
    class A:
        @OverridableProperty
        def meow(self):
            return 'bark bark!'

    a = A()
    assert a.meow == 'bark bark!'
    assert a.meow == 'bark bark!'
    assert a.meow == 'bark bark!'
    a.meow = 'Meow indeed, ma chérie.'
    assert a.meow == 'Meow indeed, ma chérie.'


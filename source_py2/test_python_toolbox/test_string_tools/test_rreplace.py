# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox.string_tools import rreplace


def test():
    assert rreplace('meow meow meow', 'meow', 'woof') == \
           rreplace('meow meow meow', 'meow', 'woof', 3) == \
           rreplace('meow meow meow', 'meow', 'woof', 3000) == 'woof woof woof'
    
    assert rreplace('meow meow meow', 'meow', 'woof', 2) == 'meow woof woof'
    assert rreplace('meow meow meow', 'meow', 'woof', 1) == 'meow meow woof'
    assert rreplace('meow meow meow', 'meow', 'woof', 0) == 'meow meow meow'
    
    assert rreplace('aaa', 'aa', 'AA') == rreplace('aaa', 'aa', 'AA', 1) == \
                                                                          'aAA'
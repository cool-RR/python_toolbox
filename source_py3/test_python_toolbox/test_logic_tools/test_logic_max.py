# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

import itertools

from python_toolbox.logic_tools import logic_max


def test():
    '''Test the basic working of `logic_max`.'''
    assert logic_max(list(range(4))) == [3]
    assert logic_max(set(range(5))) == [4]
    assert logic_max(iter(list(range(6)))) == [5]
    assert logic_max(tuple(range(10))) == [9]
    
    class FunkyString:
        def __init__(self, string):
            self.string = string
            
        def __ge__(self, other):
            assert isinstance(other, FunkyString)
            return other.string in self.string
        
        def __eq__(self, other):
            assert isinstance(other, FunkyString)
            return other.string == self.string
        
    assert logic_max(
        [FunkyString('meow'),
         FunkyString('meow frr'),
         FunkyString('ow')]
    ) == [FunkyString('meow frr')]
    
    assert logic_max(
        [FunkyString('meow'),
         FunkyString('meow frr'),
         FunkyString('ow'),
         FunkyString('Stanislav')]
    ) == []
    
    assert logic_max(
        [FunkyString('meow'),
         FunkyString('meow frr'),
         FunkyString('ow'),
         FunkyString('meow frr')]
    ) == [FunkyString('meow frr'), FunkyString('meow frr'),]

    
    class FunkyInt:
        def __init__(self, number):
            self.number = number
        def __ge__(self, other):
            return (10 <= self.number <= 20)
        def __eq__(self, other):
            assert isinstance(other, FunkyInt)
            return other.number == self.number
        
    assert logic_max(
        [FunkyInt(7),
         FunkyInt(13),
         FunkyInt(3),
         FunkyInt(18),
         FunkyInt(24),]
    ) == [FunkyInt(13), FunkyInt(18)]
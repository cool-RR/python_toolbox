# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import nose

from python_toolbox.nifty_collections import CuteEnum


def test():
    class Flavor(CuteEnum):
        CHOCOLATE = 'chocolate'
        VANILLA = 'vanilla'
        RASPBERRY = 'raspberry'
        BANANA = 'banana'
        
    assert tuple(Flavor) == (Flavor.CHOCOLATE, Flavor.VANILLA,
                             Flavor.RASPBERRY, Flavor.BANANA)
    
    assert sorted((Flavor.VANILLA, Flavor.RASPBERRY, Flavor.RASPBERRY,
                   Flavor.CHOCOLATE)) == [
        Flavor.CHOCOLATE, Flavor.VANILLA, Flavor.RASPBERRY, Flavor.RASPBERRY, 
    ]
    
    assert Flavor.VANILLA.number == 1
    
    assert Flavor.VANILLA == Flavor.VANILLA
    assert Flavor.VANILLA <= Flavor.VANILLA
    assert Flavor.VANILLA >= Flavor.VANILLA
    assert not (Flavor.VANILLA < Flavor.VANILLA)
    assert not (Flavor.VANILLA > Flavor.VANILLA)
        
    assert not (Flavor.VANILLA == Flavor.RASPBERRY)
    assert Flavor.VANILLA <= Flavor.RASPBERRY
    assert not (Flavor.VANILLA >= Flavor.RASPBERRY)
    assert Flavor.VANILLA < Flavor.RASPBERRY
    assert not (Flavor.VANILLA > Flavor.RASPBERRY)
        
    assert Flavor[2] == Flavor.RASPBERRY
    assert Flavor[:2] == (Flavor.CHOCOLATE, Flavor.VANILLA)
        
            

def test_comparable_enum_recipe():
    class ComparableEnum(CuteEnum):
        def __eq__(self, other):
            if type(other) == type(self):
                return self is other
            elif isinstance(other, str):
                return self.value == other
            else:
                return NotImplemented
            
        __str__ = lambda self: self.value
    
    class Style(ComparableEnum):
        ROCK = 'rock'
        JAZZ = 'jazz'
        BLUES = 'blues'
        
        
    assert Style.ROCK == Style.ROCK == str(Style.ROCK) == 'rock'
    assert 'jazz' != Style.ROCK != Style.JAZZ
    assert Style.ROCK != Style.ROCK.number == 0
    
    assert sorted(Style) == [Style.ROCK, Style.JAZZ, Style.BLUES]
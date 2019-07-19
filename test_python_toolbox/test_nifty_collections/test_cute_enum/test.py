# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

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



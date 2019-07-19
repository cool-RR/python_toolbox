# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox.nifty_collections import WeakKeyDefaultDict
from python_toolbox import gc_tools


class WeakreffableObject:
    ''' '''
    def __lt__(self, other):
        # Arbitrary sort order for testing.
        return id(self) < id(other)


def test():
    '''Test the basic workings of `WeakKeyDefaultDict`.'''
    wkd_dict = WeakKeyDefaultDict(default_factory=lambda: 7)

    weakreffable_object_0 = WeakreffableObject()
    weakreffable_object_1 = WeakreffableObject()
    weakreffable_object_2 = WeakreffableObject()
    weakreffable_object_3 = WeakreffableObject()

    wkd_dict[weakreffable_object_0] = 2
    assert wkd_dict[weakreffable_object_0] == 2
    assert wkd_dict[weakreffable_object_1] == 7
    assert wkd_dict[weakreffable_object_2] == 7

    assert weakreffable_object_0 in wkd_dict
    assert weakreffable_object_1 in wkd_dict
    assert weakreffable_object_2 in wkd_dict
    assert 'meow' not in wkd_dict

    assert sorted(wkd_dict.items()) == sorted(wkd_dict.items()) == sorted(
        ((weakreffable_object_0, 2),
         (weakreffable_object_1, 7),
         (weakreffable_object_2, 7), )
    )

    assert set(wkd_dict.iterkeys()) == set(wkd_dict.keys()) == \
           {ref() for ref in wkd_dict.iterkeyrefs()} == \
           {ref() for ref in wkd_dict.keyrefs()} == \
           {weakreffable_object_0, weakreffable_object_1, weakreffable_object_2}

    weakreffable_object_3 = WeakreffableObject()
    wkd_dict[weakreffable_object_3] = 123
    assert len(list(wkd_dict.keys())) == 4
    del weakreffable_object_3
    gc_tools.collect()
    assert len(list(wkd_dict.keys())) == 3

    assert wkd_dict.pop(weakreffable_object_2) == 7
    assert len(wkd_dict) == 2
    popped_key, popped_value = wkd_dict.popitem()
    assert popped_key in (weakreffable_object_0, weakreffable_object_1)
    assert popped_value in (2, 7)


    weakreffable_object_4 = WeakreffableObject()
    weakreffable_object_5 = WeakreffableObject()
    weakreffable_object_6 = WeakreffableObject()

    assert weakreffable_object_4 not in wkd_dict
    wkd_dict.setdefault(weakreffable_object_4, 222)
    assert wkd_dict[weakreffable_object_4] == 222

    wkd_dict.update({weakreffable_object_5: 444,})
    assert wkd_dict[weakreffable_object_5] == 444
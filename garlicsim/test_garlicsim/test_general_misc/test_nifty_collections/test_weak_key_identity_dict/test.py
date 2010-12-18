import nose

from garlicsim.general_misc.nifty_collections import WeakKeyIdentityDict


class WeakreffableList(list):
    pass


def test():
    wki_dict = WeakKeyIdentityDict()
    my_weakreffable_list = WeakreffableList([1, 2])
    wki_dict[my_weakreffable_list] = 7
    assert my_weakreffable_list in wki_dict
    assert wki_dict[my_weakreffable_list] == 7
    identical_weakreffable_list = WeakreffableList([1, 2])
    assert identical_weakreffable_list not in wki_dict
    nose.tools.assert_raises(KeyError,
                             lambda: wki_dict[identical_weakreffable_list])
    
    my_weakreffable_list.append(3)
    assert my_weakreffable_list in wki_dict
    assert wki_dict[my_weakreffable_list] == 7
    
    del wki_dict[my_weakreffable_list]
    assert my_weakreffable_list not in wki_dict
    nose.tools.assert_raises(KeyError,
                             lambda: wki_dict[my_weakreffable_list])
from garlicsim.general_misc.arguments_profile import ArgumentsProfile
from garlicsim.general_misc.third_party.ordered_dict import OrderedDict


def test_only_defaultless():
    def func(a, b, c):
        pass
    
    a1 = ArgumentsProfile(func, 1, 2, 3)
    assert a1.args == (1, 2, 3)
    assert not a1.kwargs
    
    a2 = ArgumentsProfile(func, 1, c=3, b=2)
    a3 = ArgumentsProfile(func, c=3, a=1, b=2)
    a4 = ArgumentsProfile(func, 1, **{'c': 3, 'b': 2})
    a5 = ArgumentsProfile(func, **OrderedDict((('c', 3), ('b',  2), ('a',  1))))
    assert a1 == a2 == a3 == a4 == a5
    
    
def test_simplest_defaultful():
    def func(a, b, c='three', d='four'):
        pass
    
    a1 = ArgumentsProfile(func, 'one', 'two')
    assert a1.args == ('one', 'two')
    assert not a1.kwargs
    
    a2 = ArgumentsProfile(func, 'one', 'two', 'three')
    a3 = ArgumentsProfile(func, 'one', 'two', 'three', 'four')
    assert a1 == a2 == a3
    
    a4 = ArgumentsProfile(func, 'one', 'two', 'dynamite')
    assert a1 != a4
    assert a4.args == ('one', 'two', 'dynamite')
    assert not a4.kwargs
    
    a5 = ArgumentsProfile(func, 'one', 'two', c='dynamite')
    a6 = ArgumentsProfile(func, 'one', 'two', 'dynamite', 'four')
    a7 = ArgumentsProfile(func, 'one', 'two', c='dynamite', d='four')
    a8 = ArgumentsProfile(func, 'one', 'two', 'dynamite', d='four')
    a9 = ArgumentsProfile(func, a='one', b='two', c='dynamite', d='four')
    a10 = ArgumentsProfile(func, d='four', c='dynamite', b='two', a='one')
    a11 = ArgumentsProfile(func, 'one', c='dynamite', d='four', b='two')
    assert a4 == a5 == a6 == a7 == a8 == a9 == a10 == a11
    
    a12 = ArgumentsProfile(func, 'one', 'two', d='bang')
    assert a12.args == ('one', 'two')
    assert a12.kwargs == OrderedDict((('d', 'bang'),))
    
    a13 = ArgumentsProfile(func, 'one', 'two', 'three', d='bang')
    a14 = ArgumentsProfile(func, 'one', 'two', c='three', d='bang')
    a15 = ArgumentsProfile(func, 'one', 'two', 'three', 'bang')
    a16 = ArgumentsProfile(func, a='one', b='two', c='three', d='bang')
    a17 = ArgumentsProfile(func, b='two', c='three', d='bang', a='one')
    assert a13 == a14 == a15 == a16 == a17
        
    
def test_defaultful_long_first():
    def func(a, b, creativity=3, d=4):
        pass
    
    a1 = ArgumentsProfile(func, 1, 2)
    assert a1.args == (1, 2)
    assert not a1.kwargs
    
    a2 = ArgumentsProfile(func, 1, 2, 3, 4)
    a3 = ArgumentsProfile(func, a=1, b=2, creativity=3, d=4)
    a4 = ArgumentsProfile(func, creativity=3, d=4, a=1, b=2)
    a5 = ArgumentsProfile(func, 1, 2, creativity=3, d=4)
    assert a1 == a2 == a3 == a4 == a5
    
    a6 = ArgumentsProfile(func, 1, 2, d='booyeah')
    assert a6.args == (1, 2)
    assert a6.kwargs == OrderedDict((('d', 'booyeah'),))
    
    a7 = ArgumentsProfile(func, 1, 2, 3, 'booyeah')
    a8 = ArgumentsProfile(func, 1, 2, creativity=3, d='booyeah')
    assert a6 == a7 == a8
    
    
def test_defaultful_long_last():
    def func(a, b, c=3, dragon=4):
        pass
    
    a1 = ArgumentsProfile(func, 1, 2)
    assert a1.args == (1, 2)
    assert not a1.kwargs
    
    a2 = ArgumentsProfile(func, 1, 2, 3, 4)
    a3 = ArgumentsProfile(func, a=1, b=2, c=3, dragon=4)
    a4 = ArgumentsProfile(func, c=3, dragon=4, a=1, b=2)
    a5 = ArgumentsProfile(func, 1, 2, c=3, dragon=4)
    assert a1 == a2 == a3 == a4 == a5
    
    a6 = ArgumentsProfile(func, 1, 2, dragon='booyeah')
    assert a6.args == (1, 2, 3, 'booyeah')
    assert not a6.kwargs
    
    a7 = ArgumentsProfile(func, 1, 2, 3, 'booyeah')
    a8 = ArgumentsProfile(func, 1, 2, c=3, dragon='booyeah')
    assert a6 == a7 == a8
    
    
def test_many_defaultfuls_some_long():
    def func(a, b, c=3, dragon=4, e=5, f=6, glide=7, human=8):
        pass
        
    a1 = ArgumentsProfile(func, 1, 2, glide='boom')
    assert a1.args == (1, 2)
    assert a1.kwargs == OrderedDict((('glide', 'boom'),))
    
    a2 = ArgumentsProfile(func, 1, 2, 3, 4, 5, 6, 'boom')
    a3 = ArgumentsProfile(func, 1, 2, 3, glide='boom')
    assert a1 == a2 == a3
    
    a4 = ArgumentsProfile(func, 1, 2, glide='boom', human='pow')
    a5 = ArgumentsProfile(func, 1, 2, 3, 4, 5, 6, 'boom', 'pow')
    # edge case, second priority
    assert a4.args == (1, 2)
    assert a4.kwargs == OrderedDict((('glide', 'boom'), ('human', 'pow')))
    assert a4 == a5
    
    
def test_many_defaultfuls_some_long_2():
    def func(a, b, c=3, dragon=4, e=5, f=6, glide=7, human=8, iris=9):
        pass
        
    a1 = ArgumentsProfile(func, 1, 2, glide='boom')
    assert a1.args == (1, 2)
    assert a1.kwargs == OrderedDict((('glide', 'boom'),))
    
    a2 = ArgumentsProfile(func, 1, 2, 3, 4, 5, 6, 'boom')
    a3 = ArgumentsProfile(func, 1, 2, 3, glide='boom')
    assert a1 == a2 == a3
    
    a4 = ArgumentsProfile(func, 1, 2, glide='boom', human='pow', iris='badabang')
    a5 = ArgumentsProfile(func, 1, 2, 3, 4, 5, 6, 'boom', 'pow', 'badabang')
    assert a4 == a5
    assert a4.args == (1, 2, 3, 4, 5, 6, 'boom', 'pow', 'badabang')
    assert not a4.kwargs
    
    
def test_defaultful_and_star_args():
    def func(a, b, c=3, draconian=4, *args):
        pass
        
    a1 = ArgumentsProfile(func, 1, 2)
    assert a1.args == (1, 2)
    assert not a1.kwargs
    
    a2 = ArgumentsProfile(func, 1, 2, draconian='kapow')
    assert a2.args == (1, 2, 3, 'kapow')
    assert not a2.kwargs
    
    a3 = ArgumentsProfile(func, 1, 2, 3, 'kapow')
    assert a2 == a3
    
    a4 = ArgumentsProfile(func, 1, 2, 3, 'kapow', 'meow_frr')
    assert a4.args == (1, 2, 3, 'kapow', 'meow_frr')
    assert not a4.kwargs
    
    
def test_many_defaultfuls_and_star_args():
    def func(a, b, c='three', d='four', e='five', f='six', *args):
        pass
    
    a1 = ArgumentsProfile(func, 'one', 'two', f='roar')
    assert a1.args == ('one', 'two')
    assert a1.kwargs == OrderedDict((('f', 'roar'),))
    
    a2 = ArgumentsProfile(func, 'one', 'two', 'three', 'four', 'five', 'roar')
    assert a1 == a2
        
    # Specifying *args, so can't specify pre-*args arguments by keyword:
    a3 = ArgumentsProfile(func, 'one', 'two', 'three', 'four', 'five', 'roar',
                          'meow_frr')
    assert a3.args == ('one', 'two', 'three', 'four', 'five', 'roar',
                       'meow_frr')
    assert not a3.kwargs
    
    
def test_defaultfuls_and_star_kwargs():
    def func(a, b, c=3, d=4, **kwargs):
        pass
    
    a1 = ArgumentsProfile(func, 1, 2)
    assert a1.args == (1, 2)
    assert not a1.kwargs
    
    # Alphabetic ordering among the **kwargs, but `d` is first because it's a
    # non-star:
    a2 = ArgumentsProfile(func, 1, 2, d='bombastic', zany=True, blue=True)
    assert a2.args == (1, 2)
    assert a2.kwargs == OrderedDict(
        (('d', 'bombastic'), ('blue', True), ('zany', True))
    )
    
    a3 = ArgumentsProfile(func, 1, b=2, blue=True, d='bombastic', zany=True)
    a4 = ArgumentsProfile(func, zany=True, a=1, b=2, blue=True, d='bombastic')
    a5 = ArgumentsProfile(func, 1, 2, 3, 'bombastic', zany=True, blue=True)
    assert a2 == a3 == a4
    

def test_many_defaultfuls_and_star_args_and_star_kwargs():    
    def func(a, b, c='three', d='four', e='five', f='six', *args, **kwargs):
        pass
    
    a1 = ArgumentsProfile(func, 'one', 'two', f='boomboomboom', __awesome=True,
                          big=True)
    assert a1.args == ('one', 'two')
    assert a1.kwargs == OrderedDict(
        (('f', 'boomboomboom'), ('big', True), ('__awesome', True))
    )
    
    a2 = ArgumentsProfile(func, 'one', 'two', 'three', 'four', 'five',
                          'bombastic', 'meow_frr', __funky=None, zany=True,
                          _wet=False, blue=True)
    assert a2.args == ('one', 'two', 'three', 'four', 'five', 'bombastic',
                       'meow_frr')
    assert a2.kwargs == OrderedDict(
        (('blue', True), ('zany', True), ('_wet', False), ('__funky', None))
    )

    
def test_method_equality():
    # This tests for a bug where functions are compared with `is` instead of
    # `==`, which causes failure with both bound and unbound methods.
    
    class C(object):
        def my_method(self, *args):
            pass

    c1 = C()
    c2 = C()
        
    assert ArgumentsProfile(C.my_method, c1) == \
           ArgumentsProfile(C.my_method, c1)
    
    assert ArgumentsProfile(C.my_method, c1, 7, 'meow') == \
           ArgumentsProfile(C.my_method, c1, 7, 'meow')
    
    assert ArgumentsProfile(C.my_method, c1) != \
           ArgumentsProfile(C.my_method, c1, 7, 'meow')
    
    
    
    assert ArgumentsProfile(C.my_method, c1) != ArgumentsProfile(c1.my_method)
    
    assert ArgumentsProfile(C.my_method, c2) != ArgumentsProfile(c1.my_method)
    
    assert ArgumentsProfile(c1.my_method) == ArgumentsProfile(c1.my_method)
    
    assert ArgumentsProfile(c1.my_method, 7, 'meow') == \
           ArgumentsProfile(c1.my_method, 7, 'meow')
    
    assert ArgumentsProfile(c1.my_method) != ArgumentsProfile(c1.my_method, 7, 'meow')
    
    assert ArgumentsProfile(c1.my_method) != ArgumentsProfile(c2.my_method)
    
    assert ArgumentsProfile(c1.my_method, 7, 'meow') != \
           ArgumentsProfile(c2.my_method, 7, 'meow')
    

def test_unhashable():
    def func(a, b, c=3, d=4, **kwargs):
        pass
    
    a1 = ArgumentsProfile(func, 7, {1: 2})
    assert a1.args == (7, {1: 2})
    assert not a1.kwargs
    hash(a1)
    
    a2 = ArgumentsProfile(func, 7, ({'a': 'b'},), set([1, (3, 4)]),
                          meow=[1, 2, {1: [1, 2]}])
    assert a2.args == (7, ({'a': 'b'},), set([1, (3, 4)]))
    assert a2.kwargs == OrderedDict(
        (('meow', [1, 2, {1: [1, 2]}]),)
    )
    
    a3 = ArgumentsProfile(func, *(), b=({'a': 'b'},), c=set([1, (3, 4)]), a=7,
                          meow=[1, 2, {1: [1, 2]}])
    assert a2.args == (7, ({'a': 'b'},), set([1, (3, 4)]))
    assert a2.kwargs == OrderedDict(
        (('meow', [1, 2, {1: [1, 2]}]),)
    )
    assert hash(a2) == hash(a3)
# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Run generic weakref tests on `WeakKeyIdentityDict`.'''

import gc
import sys
import unittest
import collections
import weakref
import operator

from test_python_toolbox.third_party import forked_mapping_tests

from python_toolbox import gc_tools

from python_toolbox.nifty_collections import WeakKeyIdentityDict

# Used in ReferencesTestCase.test_ref_created_during_del() .
ref_from_del = None

class C:
    def method(self):
        pass


class Callable:
    bar = None

    def __call__(self, x):
        self.bar = x


def create_function():
    def f(): pass
    return f

def create_bound_method():
    return C().method

def create_unbound_method():
    return C.method


class TestBase(unittest.TestCase):

    def setUp(self):
        self.cbcalled = 0

    def callback(self, ref):
        self.cbcalled += 1



class Object:
    def __init__(self, arg):
        self.arg = arg
    def __repr__(self):
        return "<Object %r>" % self.arg


class MappingTestCase(TestBase):

    COUNT = 10

    def test_make_weak_keyed_dict_from_dict(self):
        o = Object(3)
        dict = WeakKeyIdentityDict({o:364})
        self.assertTrue(dict[o] == 364)

        
    def test_make_weak_keyed_dict_from_weak_keyed_dict(self):
        o = Object(3)
        dict1 = WeakKeyIdentityDict({o:364})
        dict2 = WeakKeyIdentityDict(dict1)
        self.assertTrue(dict1[o] == 364)

        
    def make_weak_keyed_dict(self):
        dict_ = WeakKeyIdentityDict()
        objects = list(map(Object, list(range(self.COUNT))))
        for o in objects:
            dict_[o] = o.arg
        return dict_, objects


    def test_weak_keyed_dict_popitem(self):
        key1, value1, key2, value2 = C(), "value 1", C(), "value 2"
        weakdict = WeakKeyIdentityDict()
        weakdict[key1] = value1
        weakdict[key2] = value2
        self.assertTrue(len(weakdict) == 2)
        k, v = weakdict.popitem()
        self.assertTrue(len(weakdict) == 1)
        if k is key1:
            self.assertTrue(v is value1)
        else:
            self.assertTrue(v is value2)
        k, v = weakdict.popitem()
        self.assertTrue(len(weakdict) == 0)
        if k is key1:
            self.assertTrue(v is value1)
        else:
            self.assertTrue(v is value2)

        
    def test_weak_keyed_dict_setdefault(self):
        key, value1, value2 = C(), "value 1", "value 2"
        self.assertTrue(value1 is not value2,
                        "invalid test"
                        " -- value parameters must be distinct objects")
        weakdict = WeakKeyIdentityDict()
        o = weakdict.setdefault(key, value1)
        assert o is value1
        assert key in weakdict
        assert weakdict.get(key) is value1
        assert weakdict[key] is value1

        o = weakdict.setdefault(key, value2)
        assert o is value1
        assert key in weakdict
        assert weakdict.get(key) is value1
        assert weakdict[key] is value1

        
    def test_update(self):
        #
        #  This exercises d.update(), len(d), d.keys(), in d,
        #  d.get(), d[].
        #
        dict_ = {C(): 1, C(): 2, C(): 3}
        weakdict = WeakKeyIdentityDict()
        weakdict.update(dict_)
        self.assertEqual(len(weakdict), len(dict_))
        for k in list(weakdict.keys()):
            assert k in dict_
            v = dict_.get(k)
            assert v is weakdict[k]
            assert v is weakdict.get(k)
        for k in list(dict_.keys()):
            assert k in weakdict
            v = dict_[k]
            assert v is weakdict[k]
            assert v is weakdict.get(k)
            
        
    def test_weak_keyed_delitem(self):
        d = WeakKeyIdentityDict()
        o1 = Object('1')
        o2 = Object('2')
        d[o1] = 'something'
        d[o2] = 'something'
        self.assertTrue(len(d) == 2)
        del d[o1]
        self.assertTrue(len(d) == 1)
        self.assertTrue(list(d.keys()) == [o2])


    def test_weak_keyed_bad_delitem(self):
        d = WeakKeyIdentityDict()
        o = Object('1')
        # An attempt to delete an object that isn't there should raise
        # KeyError.  It didn't before 2.3.
        self.assertRaises(KeyError, d.__delitem__, o)
        self.assertRaises(KeyError, d.__getitem__, o)

        # If a key isn't of a weakly referencable type, __getitem__ and
        # __setitem__ raise TypeError.  __delitem__ should too.
        self.assertRaises(TypeError, d.__delitem__,  13)
        self.assertRaises(TypeError, d.__getitem__,  13)
        self.assertRaises(TypeError, d.__setitem__,  13, 13)

        
    def test_weak_keyed_cascading_deletes(self):
        # SF bug 742860.  For some reason, before 2.3 __delitem__ iterated
        # over the keys via self.data.iterkeys().  If things vanished from
        # the dict during this (or got added), that caused a RuntimeError.

        d = WeakKeyIdentityDict()
        mutate = False

        class C(object):
            def __init__(self, i):
                self.value = i
            def __hash__(self):
                return hash(self.value)
            def __eq__(self, other):
                if mutate:
                    # Side effect that mutates the dict, by removing the
                    # last strong reference to a key.
                    del objs[-1]
                return self.value == other.value

        objs = [C(i) for i in range(4)]
        for o in objs:
            d[o] = o.value
        del o   # now the only strong references to keys are in objs
        # Find the order in which iterkeys sees the keys.
        objs = list(d.keys())
        # Reverse it, so that the iteration implementation of __delitem__
        # has to keep looping to find the first object we delete.
        objs.reverse()

        # Turn on mutation in C.__eq__.  The first time thru the loop,
        # under the iterkeys() business the first comparison will delete
        # the last item iterkeys() would see, and that causes a
        #     RuntimeError: dictionary changed size during iteration
        # when the iterkeys() loop goes around to try comparing the next
        # key.  After this was fixed, it just deletes the last object *our*
        # "for o in obj" loop would have gotten to.
        mutate = True
        count = 0
        for o in objs:
            count += 1
            del d[o]
        gc_tools.collect()
        self.assertEqual(len(d), 0)
        self.assertEqual(count, 2)

        
class WeakKeyIdentityDictTestCase(
    forked_mapping_tests.BasicTestMappingProtocol
    ):
    """Check that WeakKeyDictionary conforms to the mapping protocol"""
    __ref = {Object("key1"):1, Object("key2"):2, Object("key3"):3}
    type2test = WeakKeyIdentityDict
    def _reference(self):
        return self.__ref.copy()


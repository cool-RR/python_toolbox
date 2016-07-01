# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import threading
import uuid as uuid_module

from python_toolbox import caching
from python_toolbox.caching import CachedType
from python_toolbox import nifty_collections

        
def test():
    '''Test basic workings of `CachedType`.'''
    class A(metaclass=CachedType):
        def __init__(self, a=1, b=2, *args, **kwargs):
            pass
        
    assert A() is A(1) is A(b=2) is A(1, 2) is A(1, b=2)
    assert A() is not A(3) is not A(b=7) is not A(1, 2, 'meow') is not A(x=9)
    
    
def test_thread_safe():
    
    class Feline(metaclass=CachedType):
        def __init__(self, name):
            self.name = name
            self.uuid = uuid_module.uuid4().hex
            self.creation_hook()
            
        def creation_hook(self):
            condition_list.wait_for('%s_creation' % self.name, remove=True)
            
    condition_list = nifty_collections.ConditionList()
    
    class BaseThread(threading.Thread):
        def __init__(self):
            super().__init__()

    class FirstThread(BaseThread):
        def run(self):
            condition_list.wait_for('t1go', remove=True)
            self.cat = Feline('cat')
            condition_list.append('t1done')

    class SecondThread(BaseThread):
        def run(self):
            condition_list.wait_for('t2go', remove=True)
            self.tiger = Feline('tiger')
            condition_list.append('t2done')

    class ThirdThread(BaseThread):
        def run(self):
            condition_list.wait_for('t3go', remove=True)
            self.cat = Feline('cat')
            condition_list.append('t3done')
            
    class FourthThread(BaseThread):
        def run(self):
            condition_list.wait_for('t4go', remove=True)
            self.tiger = Feline('tiger')
            condition_list.append('t4done')
            
    threads = (FirstThread(), SecondThread(), ThirdThread(), FourthThread())
    for thread in threads:
        thread.start()
    
    
    condition_list.play_out(['t1go'])
    
    cache = Feline._CachedType__cache
    assert len(cache) == 1
    ((cat_key, cat_value),) = cache.items()
    assert isinstance(cat_value, caching.cached_type.InConstructionMarker)
    assert cat_value.lock.locked()
    assert not Feline._CachedType__quick_lock.locked()
    
    condition_list.play_out(['t2go'])
    
    assert len(cache) == 2
    ((key_1, value_1), (key_2, value_2)) = cache.items()
    cat_value, tiger_value = ((value_1, value_2) if (key_1 is cat_key)
                              else (value_2, value_1))
    assert isinstance(cat_value, caching.cached_type.InConstructionMarker)
    assert cat_value.lock.locked()
    assert isinstance(tiger_value, caching.cached_type.InConstructionMarker)
    assert tiger_value.lock.locked()
    assert not Feline._CachedType__quick_lock.locked()
    
    condition_list.play_out(['tiger_creation'])
    condition_list.wait_for('t2done', remove=True)
    
    assert len(cache) == 2
    ((key_1, value_1), (key_2, value_2)) = cache.items()
    cat_value, tiger_value = ((value_1, value_2) if (key_1 is cat_key)
                              else (value_2, value_1))
    assert isinstance(tiger_value, Feline)
    assert isinstance(cat_value, caching.cached_type.InConstructionMarker)
    assert cat_value.lock.locked()
    assert not Feline._CachedType__quick_lock.locked()
    
    condition_list.play_out(['t3go'])

    assert len(cache) == 2
    ((key_1, value_1), (key_2, value_2)) = cache.items()
    cat_value, tiger_value = ((value_1, value_2) if (key_1 is cat_key)
                              else (value_2, value_1))
    assert isinstance(tiger_value, Feline)
    assert isinstance(cat_value, caching.cached_type.InConstructionMarker)
    assert cat_value.lock.locked()
    assert not Feline._CachedType__quick_lock.locked()
    
    condition_list.play_out(['cat_creation'])
    condition_list.wait_for('t1done', 't3done', remove=True)

    assert len(cache) == 2
    ((key_1, value_1), (key_2, value_2)) = cache.items()
    cat_value, tiger_value = ((value_1, value_2) if (key_1 is cat_key)
                              else (value_2, value_1))
    assert isinstance(tiger_value, Feline)
    assert isinstance(cat_value, Feline)
    
    condition_list.play_out(['t4go'])
    condition_list.wait_for('t4done', remove=True)
    assert not condition_list
    
    assert len(cache) == 2
    ((key_1, value_1), (key_2, value_2)) = cache.items()
    cat_value, tiger_value = ((value_1, value_2) if (key_1 is cat_key)
                              else (value_2, value_1))
    assert isinstance(tiger_value, Feline)
    assert isinstance(cat_value, Feline)
    
    for thread in threads:
        thread.join()
    
    assert threads[0].cat is threads[2].cat
    assert threads[0].cat.uuid == threads[2].cat.uuid
    assert threads[1].tiger is threads[3].tiger
    assert threads[1].tiger.uuid == threads[3].tiger.uuid
    
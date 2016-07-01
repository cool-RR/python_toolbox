# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import threading
import uuid as uuid_module

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

    class SecondThread(BaseThread):
        def run(self):
            condition_list.wait_for('t2go', remove=True)
            self.tiger = Feline('tiger')

    class ThirdThread(BaseThread):
        def run(self):
            condition_list.wait_for('t3go', remove=True)
            self.cat = Feline('cat')
            
    class FourthThread(BaseThread):
        def run(self):
            condition_list.wait_for('t4go', remove=True)
            self.tiger = Feline('tiger')
            
    threads = (FirstThread(), SecondThread(), ThirdThread(), FourthThread())
    for thread in threads:
        thread.start()
    
    
    condition_list.play_out(['t1go', 't2go', 'tiger_creation', 't3go',
                             'cat_creation', 't4go'])
    
    for thread in threads:
        thread.join()
    
    assert threads[0].cat is threads[2].cat
    assert threads[0].cat.uuid == threads[2].cat.uuid
    assert threads[1].tiger is threads[3].tiger
    assert threads[1].tiger.uuid == threads[3].tiger.uuid
    
    # blocktodo be asserting the in construction marker
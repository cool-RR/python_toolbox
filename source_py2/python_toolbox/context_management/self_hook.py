# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

class SelfHook(object):
    '''
    Hook that a context manager can yield in order to yield itself.

    This is useful in context managers which are created from a generator
    function, where the user can't do `yield self` because `self` doesn't exist
    yet.
    
    Example:
    
        @ContextGeneratorType
        def MyContextManager(lock):
            with lock.read:
                yield SelfHook
                
        with MyContextManager(my_lock) as my_context_manager:
            assert isinstance(my_context_manager, MyContextManager)
    
    '''
    # todo: make uninstantiable





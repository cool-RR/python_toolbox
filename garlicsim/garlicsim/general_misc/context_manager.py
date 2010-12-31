# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `ContextManager` class.

See its documentation for more information.
'''
# todo: use tests of contextlib too
# todo: test on pypy

import types

from garlicsim.general_misc.third_party import decorator as decorator_module

from garlicsim.general_misc import misc_tools
from garlicsim.general_misc import monkeypatching_tools


class ContextManagerType(type):
    def __new__(mcls, *args, **kwargs):
        type_ = super(ContextManagerType, mcls).__new__(mcls, *args, **kwargs)
    
        mro_depth_of_run = \
            misc_tools.get_mro_depth_of_method(type_, 'run')
        mro_depth_of_enter = \
            misc_tools.get_mro_depth_of_method(type_, '__enter__')
        mro_depth_of_exit = \
            misc_tools.get_mro_depth_of_method(type_, '__exit__')
        
        assert mro_depth_of_enter == mro_depth_of_exit != \
            mro_depth_of_run        
        
        if mro_depth_of_run < mro_depth_of_enter:
            type_._use_generator_for_context_management()
        
        return result

    
    def _use_generator_for_context_management(cls):
        
        @monkeypatching_tools.monkeypatch_method(type_)
        def __enter__(self):
            assert self._generator is None
            self._generator = self.run()
            assert isinstance(self._generator, types.GeneratorType)
            
            try:
                return self._generator.next()
            except StopIteration:
                raise RuntimeError("generator didn't yield")
        
        @monkeypatching_tools.monkeypatch_method(type_)
        def __exit__(self, type_, value, traceback):
            
            assert isinstance(self._generator, types.GeneratorType)
            
            if type_ is None:
                try:
                    self._generator.next()
                except StopIteration:
                    return
                else:
                    raise RuntimeError("generator didn't stop")
            else:
                if value is None:
                    # Need to force instantiation so we can reliably
                    # tell if we get the same exception back
                    value = type_()
                try:
                    self._generator.throw(type_, value, traceback)
                    raise RuntimeError("generator didn't stop after throw()")
                except StopIteration as exc:
                    # Suppress the exception *unless* it's the same exception that
                    # was passed to throw().  This prevents a StopIteration
                    # raised inside the "with" statement from being suppressed
                    return exc is not value
                except:
                    # only re-raise if it's *not* the exception that was
                    # passed to throw(), because __exit__() must not raise
                    # an exception unless __exit__() itself failed.  But throw()
                    # has to raise the exception to signal propagation, so this
                    # fixes the impedance mismatch between the throw() protocol
                    # and the __exit__() protocol.
                    #
                    if sys.exc_info()[1] is not value:
                        raise


class ContextManager(object):
    
    __metaclass__ = ContextManagerType
    
    def __call__(self, function):
        def inner(*args, **kwargs):
            with self:
                return function(*args, **kwargs)
        return decorator_module.decorator(inner, function)
    
    def __enter__(self):
        pass
    
    def __exit__(self, *args, **kwargs):
        pass
# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import contextlib

from python_toolbox.nifty_collections import CuteEnum

from .abstract_context_manager import AbstractContextManager
from .context_manager import ContextManager


def _get_enterer(enterable):
    enter_function = type(exitable).__enter__
    return (lambda: enter_function(enterable))
    

def _get_exiter(exitable):
    exit_function = type(exitable).__exit__
    return (
        lambda exc_type, exc_value, exc_traceback:
                    exit_function(exitable, exc_type, exc_value, exc_traceback)
    )



class StackState(CuteEnum):
    ALIVE = 0
    EXITING = 1
    EXITED = 2
        

class ThreadPoolExitStack(ContextManager):
    """
    blocktododoc
    Context manager for dynamic management of a stack of exit callbacks

    For example:

        with ExitStack() as stack:
            files = [stack.enter_context(open(fname)) for fname in filenames]
            # All opened files will automatically be closed at the end of
            # the with statement, even if attempts to open files later
            # in the list raise an exception

    """
    def __init__(self, *, executor=None, n_threads=None):
        from python_toolbox.future_tools import CuteThreadPoolExecutor
        self._exit_callbacks = deque()
        self._state = StackState.ALIVE
        if executor is None:
            self._executor = \
                 CuteThreadPoolExecutor(10 if n_threads is None else n_threads)
            self.enter_context(self._executor)
        else:
            assert n_threads is None
            self._executor = executor

    def pop_all(self):
        """Preserve the context stack by transferring it to a new instance"""
        new_stack = type(self)()
        new_stack._exit_callbacks = self._exit_callbacks
        self._exit_callbacks = deque()
        return new_stack

    def push(self, exit):
        """Registers a callback with the standard __exit__ method signature

        Can suppress exceptions the same way __exit__ methods can.

        Also accepts any object with an __exit__ method (registering a call
        to the method instead of the object itself)
        """
        # We use an unbound method rather than a bound method to follow
        # the standard lookup behaviour for special methods
        _cb_type = type(exit)
        try:
            exit_method = _cb_type.__exit__
        except AttributeError:
            # Not a context manager, so assume its a callable
            self._exit_callbacks.append(exit)
        else:
            self._push_context_manager_exit(exit, exit_method)
        return exit # Allow use as a decorator

    def callback(self, callback, *args, **kwds):
        """Registers an arbitrary callback and arguments.

        Cannot suppress exceptions.
        """
        def _exit_wrapper(exc_type, exc, tb):
            callback(*args, **kwds)
        # We changed the signature, so using @wraps is not appropriate, but
        # setting __wrapped__ may still help with introspection
        _exit_wrapper.__wrapped__ = callback
        self.push(_exit_wrapper)
        return callback # Allow use as a decorator

    def enter_context(self, context_manager):
        (result,) = self.enter_contexts((context_manager,))
        return result


    def enter_contexts(self, context_managers):
        """Enters the supplied context manager

        If successful, also pushes its __exit__ method as a callback and
        returns the result of the __enter__ method.
        """
        from python_toolbox import sequence_tools
        # We look up the special methods on the type to match the with statement
        
        def enter_in_thread(context_manager):
            enterer = _get_enterer(context_manager)
            if StackState.
            enter_value = enterer()
            self.push(_get_exiter(context_manager))
            return enter_value
        
        return tuple(self._executor.map(enter_in_thread, context_managers))

    def close(self):
        """Immediately unwind the context stack"""
        self.__exit__(None, None, None)

    def __enter__(self):
        return self

    def __exit__(self, *exc_details):
        if self._state != StackState.ALIVE:
            raise RuntimeError
        self._state = StackState.EXITING
        
        received_exc = exc_details[0] is not None

        # We manipulate the exception state so it behaves as though
        # we were actually nesting multiple with statements
        frame_exc = sys.exc_info()[1]
        def _fix_exception_context(new_exc, old_exc):
            # Context may not be correct, so find the end of the chain
            while 1:
                exc_context = new_exc.__context__
                if exc_context is old_exc:
                    # Context is already set correctly (see issue 20317)
                    return
                if exc_context is None or exc_context is frame_exc:
                    break
                new_exc = exc_context
            # Change the end of the chain to point to the exception
            # we expect it to reference
            new_exc.__context__ = old_exc

        # Callbacks are invoked in LIFO order to match the behaviour of
        # nested context managers
        suppressed_exc = False
        pending_raise = False
        while self._exit_callbacks:
            cb = self._exit_callbacks.pop()
            try:
                if cb(*exc_details):
                    suppressed_exc = True
                    pending_raise = False
                    exc_details = (None, None, None)
            except:
                new_exc_details = sys.exc_info()
                # simulate the stack of exceptions by setting the context
                _fix_exception_context(new_exc_details[1], exc_details[1])
                pending_raise = True
                exc_details = new_exc_details
        if pending_raise:
            try:
                # bare "raise exc_details[1]" replaces our carefully
                # set-up context
                fixed_ctx = exc_details[1].__context__
                raise exc_details[1]
            except BaseException:
                exc_details[1].__context__ = fixed_ctx
                raise
            
        assert self._state == StackState.EXITING
        self._state = StackState.EXITED
            
        return received_exc and suppressed_exc

import functools

from . import base_profile


def profile_ready(start_on=False, off_after=False, sort=1):
    def decorator(function):
        def decorated(*args, **kwargs):
            if decorated.profiling_on:
                if decorated.off_after:
                    decorated.profiling_on = False
                decorated.original_function # This line puts it in locals, weird
                base_profile.runctx(
                    'result = decorated.original_function(*args, **kwargs)',
                    globals(), locals(), sort=sort
                )
                return locals()['result']
            else: # decorated.profiling_on is False
                return decorated.original_function(*args, **kwargs)
        decorated.original_function = function
        decorated.off_after = off_after
        decorated.profiling_on = start_on
        functools.update_wrapper(decorated, function)
        return decorated
    return decorator




if __name__ == '__main__':
    
    @profile_ready(start_on=True)
    def f():
        import time
        time.sleep(0.01)
        return 7
    
    print f()
    
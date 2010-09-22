import cProfile
import functools

def runctx(statement, globals, locals, filename=None, sort=-1):
    """Run statement under profiler, supplying your own globals and locals,
    optionally saving results in filename.

    statement and filename have the same semantics as profile.run
    """
    prof = cProfile.Profile()
    result = None
    try:
        try:
            prof = prof.runctx(statement, globals, locals)
        except SystemExit:
            pass
    finally:
        if filename is not None:
            prof.dump_stats(filename)
        else:
            result = prof.print_stats(sort)
    return result


def decorator(function):
    def decorated(*args, **kwargs):
        decorated.original_function # This line puts it in locals, weird
        runctx('result = decorated.original_function(*args, **kwargs)',
               globals(), locals(), sort=2)
        return locals()['result']
    decorated.original_function = function
    functools.update_wrapper(decorated, function)
    return decorated

if __name__ == '__main__':
    
    @decorator
    def f():
        import time
        time.sleep(0.01)
        return 7
    
    print f()
    
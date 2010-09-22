try:
    from cProfile import *
except ImportError:
    from profile import *

def runctx(statement, globals, locals, filename=None, sort=-1):
    """Run statement under profiler, supplying your own globals and locals,
    optionally saving results in filename.

    statement and filename have the same semantics as profile.run
    """
    prof = Profile()
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
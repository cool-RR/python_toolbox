
def cannot_compile(thing):
    try:
        import psyco
    except ImportError:
        return
    
    return psyco.cannotcompile(thing)
    
    
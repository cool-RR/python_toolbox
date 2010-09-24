import weakref

def _is_weakreffable(thing):
    try:
        weakref.ref(thing)
    except TypeError:
        return False
    else:
        return True

class A(object):
    @staticmethod
    def s():
        pass

    
def counter(*args, **kwargs):
    if not hasattr(counter, 'count'):
        counter.count = 0
    result = counter.count
    counter.count += 1
    return result

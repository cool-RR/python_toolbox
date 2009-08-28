class Facade(object):
    def __init__(self, thing):
        self.__dict__ = thing.__dict__.copy()


def testy(thing):
    import cPickle
    f = Facade(thing)
    try:
        cPickle.dumps(f)
        return f
    except:
        raise
        return False

    
import garlicsimwx.simulationpackages.life as life
testy(life)
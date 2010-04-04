from garlicsim.general_misc.third_party import abc
import itertools

class EventMeta(type):
    def __new__(mcls, name, bases, namespace):
        cls = super(EventMeta, mcls).__new__(mcls, name, bases, namespace)
        cls.specific_subscribers = set()
        return cls

class Event(object):
    __metaclass__ = EventMeta
    def __init__(self, *args, **kwargs):
        self.sent = False
        self.args, self.kwargs = args, kwargs
    
    @classmethod
    def add_subscriber(cls, subscriber):
        cls.specific_subscribers.add(subscriber)
    
    @classmethod
    def remove_subscriber(cls, subscriber):
        cls.specific_subscribers.remove(subscriber)
        
    @classmethod
    def get_subscribers(cls):
        event_bases = [base for base in cls.__bases__
                       if issubclass(base, Event)] 
        
        base_subscribers = reduce(
            set.union,
            [base.get_subscribers() for base in event_bases],
            set()
        )
        # todo: Is there a more efficient way to add sets?
        
        return set.union(
            base_subscribers,
            cls.specific_subscribers
        )
    
    def send(self):
        if self.sent is True:
            raise Exception()
        self.sent = True
        for subscriber in self.get_subscribers():
            subscriber(*self.args, **self.kwargs)
    
        
if __name__ == '__main__': # todo: move this to a test
    class Violence(Event): pass
    class Explosion(Violence): pass
    class FistFight(Violence): pass
    class War(Explosion, FistFight): pass
    
    
    def violence_subscriber():
        print('Violence subscriber called')
    def explosion_subscriber():
        print('Explosion subscriber called')
    def fist_fight_subscriber():
        print('FistFight subscriber called')
    def war_subscriber():
        print('War subscriber called')
    
    Violence.add_subscriber(violence_subscriber)
    Explosion.add_subscriber(explosion_subscriber)
    FistFight.add_subscriber(fist_fight_subscriber)
    War.add_subscriber(war_subscriber)
    
    Violence().send()
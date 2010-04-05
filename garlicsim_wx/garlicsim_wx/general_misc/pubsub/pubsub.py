from garlicsim.general_misc.third_party import abc
import itertools
# todo: possibly make thread that consolidates subscriber calling.
# todo: can define "abstract" event type, so you can't create direct instances,
# only instances of subclasses. For example TreeChanged.

# Thinking aid: If event type A has subclasses B and C, it means it gets called
# if B or C get called. (Or also if it gets called directly itself.)

class EventType(type):
    # todo: can make nice __repr__
    def __new__(mcls, name='UnnamedEventType', bases=None, namespace={},
                subs=()):
        '''note that default for bases is (Event,)'''
        
        if bases is None:
            bases = (Event,)
            
        namespace = dict(namespace)
        namespace.setdefault('__metaclass__', EventType)
        
        cls = super(EventType, mcls).__new__(mcls, name, bases, namespace)
        cls.specific_subscribers = set()
        return cls
    
    def __init__(cls, name='UnnamedEventType', bases=None, namespace={},
                 subs=()):
        '''note that default for bases is (Event,)'''
        
        if bases is None:
            bases = (Event,)
            
        namespace = dict(namespace)
        namespace.setdefault('__metaclass__', EventType)
        
        for sub in subs:
            assert isinstance(sub, EventType)
            sub.__bases__ = (cls,) + sub.__bases__ # Oh yeah.
        
        cls = super(EventType, cls).__init__(name, bases, namespace)

class Event(object):
    __metaclass__ = EventType
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

        # todo: Maybe faster to iterate over the specific_subscribers of all
        # those in __mro__
        
        # todo: Is there a more efficient way to add sets?
        
        
        return set.union(
            base_subscribers,
            cls.specific_subscribers
        )
    
    def send(self):
        if self.sent is True:
            raise Exception()
        self.sent = True
        print type(self) # debug
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
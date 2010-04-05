from garlicsim.general_misc.third_party import abc
import itertools
# todo: possibly make thread that consolidates subscriber calling.
# todo: can define "abstract" event type, so you can't create direct instances,
# only instances of subclasses. For example TreeChanged.


class EventSystem(object):
    
    def __init__(self):
        
        
        self.bottom_event_type = \
            EventType('BottomEvent', (BaseEvent,), {})
        
        self.top_event_type = \
            EventType('TopEvent', (self.bottom_event_type,), {})
        
        self.event_type_set = set((
            self.bottom_event_type,
            self.top_event_type
        ))


    """
    def __make_unlinked_event_type(self, name='Unnamed'):        
        event_type = type(name, (Event,), {})
        event_type.specific_subscribers = set()
        return event_type
    """
    
    def make_event_type(self, name='Unnamed', bases=None, subs=None):
        
        if bases is None:
            bases = (self.bottom_event_type,)
        else:
            assert all(isinstance(base, type) for base in bases)
            if not any(issubclass(base, self.bottom_event_type) in bases):
                bases = (self.bottom_event_type,) + bases
                # Afraid to change to +=
        
        if subs is None:
            subs = (self.top_event_type,)
        else:
            assert all(isinstance(base, type) for sub in subs)
            if not any(issubclass(self.top_event_type, sub) in subs):
                subs = subs + (self.top_event_type,)
                # Afraid to change to +=
        
        event_type = EventType(name, bases, subs)
        
        self.event_type_set.add(event_type)
        
        return event_type
    
    def remove_event_type(self, event_type):
        assert event_type in self.event_type_set

        for other_event_type in self.event_type_set:
            if event_type in other_event_type.__bases__:
                new_bases = list(other_event_type.__bases__)
                while event_type in new_bases:
                    new_bases.remove(event_type)
                other_event_type.__bases__ = tuple(new_bases)
        
        self.event_type_set.remove(event_type)
        

# Thinking aid: If event type A has subclasses B and C, it means it gets called
# if B or C get called. (Or also if it gets called directly itself.)

class EventType(type):
    
    #__metaclass__ = EventSystem
    
    def __new__(mcls, name='Unnamed', bases=None, namespace={},
                subs=()):
        '''note that default for bases is (BaseEvent,)'''
        
        if bases is None:
            bases = (BaseEvent,)
            
        #namespace = dict(namespace)
        #namespace.setdefault('__metaclass__', EventType)
        
        
        cls = super(EventType, mcls).__new__(mcls, name, bases, namespace)
        cls.specific_subscribers = set()
        return cls
    
    def __init__(cls, name='Unnamed', bases=None, namespace={},
                 subs=()):
        '''note that default for bases is (BaseEvent,)'''
    
        
        if bases is None:
            bases = (BaseEvent,)
            
        #namespace = dict(namespace)
        #namespace.setdefault('__metaclass__', EventType)
        
        for sub in subs:
            assert issubclass(sub, BaseEvent)
            sub.__bases__ = (cls,) + sub.__bases__ # Oh yeah.
        
        cls = super(EventType, cls).__init__(name, bases, namespace)
    
    def __repr__(self):
        return '<%s EventType at %s>' % (
            self.__name__,
            hex(id(self))
            )
    

class BaseEvent(object):
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
                       if issubclass(base, BaseEvent) and
                       base is not BaseEvent] 
        
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
        print self # debug
        for subscriber in self.get_subscribers():
            subscriber(*self.args, **self.kwargs)
            
    def __repr__(self):
        return '<%s event at %s>' % (
            self.__class__.__name__,
            hex(id(self))
            )
    
        
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
    
    event_system = EventSystem()
    event_type = event_system.make_event_type()
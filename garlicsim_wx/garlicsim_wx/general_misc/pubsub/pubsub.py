from garlicsim.general_misc.third_party import abc
import itertools
from garlicsim.general_misc import cute_iter_tools
# todo: possibly make thread that consolidates subscriber calling.
# todo: can define "abstract" event type, so you can't create direct instances,
# only instances of subclasses. For example TreeChanged.

def class_cmp(a, b):
    if issubclass(a, b):
        return -1
    if issubclass(b, a):
        return 1
    else:
        return type.__cmp__(a, b)
        

def sanitize_bases(bases):
    new_bases = sorted(bases, class_cmp)
        
    kill_set = set()
    
    for first_base, second_base in \
        cute_iter_tools.orderless_combinations(new_bases, 2):
        if issubclass(first_base, second_base):
            kill_set.add(second_base)
    
    for base_to_kill in kill_set:
        new_bases.remove(base_to_kill)
    
    return tuple(new_bases)

def inject_base(cls, base): # move to other module
    """
    new_bases = [base]
    for old_base in cls.__bases__:
        if not issubclass(base, old_base):
            new_bases.append(old_base)
    """
    cls.__bases__ = sanitize_bases(cls.__bases__ + (base,))
    # All your base are belong to us.
    

class EventSystem(object):
    
    def __init__(self):
        
        
        self.bottom_event_type = \
            EventType('BottomEvent', (BaseEvent,), {})
        
        self.top_event_type = \
            EventType('TopEvent', (self.bottom_event_type,), {})
        
        self.event_types = set((
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
            bases = ()
        bases = sanitize_bases(bases + (self.bottom_event_type,))
        """
        if bases is None:
            bases = (self.bottom_event_type,)
        else:
            assert all(isinstance(base, type) for base in bases)
            if not any(issubclass(base, self.bottom_event_type)
                       for base in bases):
                bases = (self.bottom_event_type,) + bases
                # Afraid to change to +=
        """
        
        if subs is None:
            subs = (self.top_event_type,)
        else:
            assert all(isinstance(sub, type) for sub in subs)
            if not any(issubclass(self.top_event_type, sub) for sub in subs):
                subs = subs + (self.top_event_type,)
                # Afraid to change to +=
        
        event_type = EventType(name, bases=bases, subs=subs)
        
        self.event_types.add(event_type)
        
        return event_type
        
    
    
    def remove_event_type(self, event_type):

        event_type_to_remove = event_type
        assert event_type_to_remove in self.event_types
        abandoned_bases = event_type_to_remove.__bases__
        
        for other_event_type in self.event_types:
            if event_type_to_remove in other_event_type.__bases__:
                new_bases = list(other_event_type.__bases__)
                while event_type in new_bases:
                    new_bases.remove(event_type)
                new_bases += abandoned_bases
                
                other_event_type.__bases__ = sanitize_bases(new_bases)
        
        self.event_types.remove(event_type)
        

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
            inject_base(sub, cls) # Oh yeah.
        
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
    
    event_system = EventSystem()
    SocialEvent = event_system.make_event_type('SocialEvent')
    Party = event_system.make_event_type('Party', (SocialEvent,))
    MusicParty = event_system.make_event_type('MusicParty', (Party,))
    TranceMusicParty = event_system.make_event_type('TranceMusicParty', (MusicParty,))
    Dinner = event_system.make_event_type('Dinner', (SocialEvent,))
    Show = event_system.make_event_type('Show', (SocialEvent,))
    RockConcert = event_system.make_event_type('RockConcert', (MusicParty, Show))
    
    DinnerOrShow = event_system.make_event_type('DinnerOrShow', subs=(Dinner, Show))
    
    def make_subscriber(name):
        def subscriber():
            print('%s subscriber called' % name)
        return subscriber
    
    for event_type in event_system.event_types:
        event_type.add_subscriber(make_subscriber(event_type.__name__))
        
    
    def get_relations(classes):
        relations = {}
        for cls1 in classes:
            relations[cls1] = set(cls2 for cls2 in classes if issubclass(cls1, cls2))
        return relations
            
    def prune_relations(rel1, thing):
        for (key, value) in rel1.copy().iteritems():
            if (key is thing):
                del rel1[thing]
                continue
            if thing in value:
                value.remove(thing)
       
    to_remove = MusicParty
    rel = get_relations(event_system.event_types)
    prune_relations(rel, to_remove)
    event_system.remove_event_type(to_remove)
    new_rel = get_relations(event_system.event_types)
    assert new_rel == rel
        
            
            
    
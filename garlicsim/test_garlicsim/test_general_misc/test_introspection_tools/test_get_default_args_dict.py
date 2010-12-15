from garlicsim.general_misc.introspection_tools import get_default_args_dict
from garlicsim.general_misc.third_party.ordered_dict import OrderedDict

def test():
    def f(a, b, c=3, d=4):
        pass
    
    assert get_default_args_dict(f) == \
        OrderedDict((('c', 3), ('d', 4)))
    
    
def test_generator():   
    def f(a, meow='frr', d={}):
        yield None
    
    assert get_default_args_dict(f) == \
        OrderedDict((('meow', 'frr'), ('d', {})))
    
    
def test_empty():   
    def f(a, b, c, *args, **kwargs):
        pass
    
    assert get_default_args_dict(f) == \
        OrderedDict()
    
# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''This module defines miscellaneous tools.'''

import re
import math
import types

from garlicsim.general_misc import cute_iter_tools

    
def is_subclass(candidate, base_class):
    '''
    Check if `candidate` is a subclass of `base_class`.
    
    You may pass in a tuple of base classes instead of just one, and it will
    check whether `candidate` is a subclass of any of these base classes.
    
    This has 2 advantages of over the built-in `issubclass`:
    
     1. It doesn't throw an exception if `candidate` is not a type. (Python
        issue 10569.)
     2. It manually checks for a `__subclasscheck__` method on `base_class`.
        This is helpful for Python 2.5 compatibility because Python started
        using `__subclasscheck__` in its built-in `issubclass` starting from
        Python 2.6.
        
    '''
    # todo: disable ability to use nested iterables.
    if cute_iter_tools.is_iterable(base_class):
        return any(is_subclass(candidate, single_base_class) for 
                   single_base_class in base_class)
    elif not isinstance(candidate, (type, types.ClassType)):
        return False
    elif hasattr(base_class, '__subclasscheck__'):
        return base_class.__subclasscheck__(candidate)
    else:
        return issubclass(candidate, base_class)


def get_mro_depth_of_method(type_, method_name):
    '''
    Get the mro-depth of a method.
    
    This means, the index number in `type_`'s MRO of the base class that
    defines this method.
    '''
    assert isinstance(method_name, basestring)
    mro = type_.mro()
    
    assert mro[0] is type_
    method = getattr(mro[0], method_name)
    assert method is not None

    for deepest_index, base_class in reversed(list(enumerate(mro))):
        if hasattr(base_class, method_name) and \
           getattr(base_class, method_name) == method:
            break
        
    return deepest_index


def frange(start, finish=None, step=1.):
    '''
    Make a `list` containing an arithmetic progression of numbers.

    This is an extension of the builtin `range`; it allows using floating point
    numbers.
    '''
    if finish is None:
        finish, start = start, 0.
    else:
        start = float(start)

    count = int(math.ceil(finish - start)/step)
    return (start + n*step for n in range(count))
    

def getted_vars(thing, _getattr=getattr):
    '''
    The `vars` of an object, but after we used `getattr` to get them.
    
    This is useful because some magic (like descriptors or `__getattr__`
    methods) need us to use `getattr` for them to work. For example, taking
    just the `vars` of a class will show functions instead of methods, while
    the "getted vars" will have the actual method objects.
    
    You may provide a replacement for the built-in `getattr` as the `_getattr`
    argument.
    '''
    # todo: can make "fallback" option, to use value from original `vars` if
    # get is unsuccessful.
    my_vars = vars(thing)
    return dict((name, _getattr(thing, name)) for name in my_vars.iterkeys())



_ascii_variable_pattern = re.compile('^[a-zA-Z_][0-9a-zA-Z_]*$')
def is_legal_ascii_variable_name(name):
    '''Return whether `name` is a legal name for a Python variable.'''
    return bool(_ascii_variable_pattern.match(name))


def is_magic_variable_name(name):
    '''Return whether `name` is a name of a magic variable (e.g. '__add__'.)'''
    return is_legal_ascii_variable_name(name) and \
           len(name) >= 5 and \
           name[:2] == name[-2:] == '__'


def get_actual_type(thing):
    '''
    Get the actual type (or class) of an object.
    
    This is used instead of `type(thing)` for compaibility with old-style
    classes.
    '''
    
    return getattr(thing, '__class__', None) or type(thing)
    # Using `.__class__` instead of `type` because of goddamned old-style
    # classes. When you do `type` on an instance of an old-style class, you
    # just get the useless `InstanceType`. But wait, there's more! We can't
    # just take `thing.__class__` because the old-style classes themselves,
    # i.e. the classes and not the instances, do not have a `.__class__`
    # attribute at all! Therefore we are using `type` as a fallback.
    #
    # I don't like old-style classes, that's what I'm saying.
    
    
def is_number(x):
    '''Return whether `x` is a number.'''
    try:
        x + 1
    except Exception:
        return False
    else:
        return True

    
def identity_function(thing):
    '''
    Return `thing`.
    
    This function is useful when you want to use an identity function but can't
    define a lambda one because it wouldn't be pickleable. Also using this
    function might be faster as it's prepared in advance.
    '''
    return thing
    

def do_nothing(*args, **kwargs):
    pass

        
class OwnNameDiscoveringProperty(object):
    ''' '''
    def __init__(self, name=None):
        '''
        
        You may optionally pass in the name that this property has in the
        class; this will save a bit of processing later.
        '''
        self.our_name = name
    
        
    def get_our_name(self, obj, our_type=None):
        if self.our_name is not None:
            return self.our_name
        
        if not our_type:
            our_type = type(obj)
        (self.our_name,) = (name for name in dir(our_type) if
                            getattr(our_type, name, None) is self)
        
        return self.our_name
# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''This module defines miscellaneous tools.'''

from __future__ import division

import operator
import os.path
import re
import math
import types

from python_toolbox import cute_iter_tools


_email_pattern = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016'
    r'-\177])*"'
    r')@((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|'
    r'[A-Z0-9-]{2,}\.?)$)'
    r'|\[(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|'
    r'[0-1]?\d?\d)){3}\]$',
    re.IGNORECASE
)

    
def is_subclass(candidate, base_class):
    '''
    Check if `candidate` is a subclass of `base_class`.
    
    You may pass in a tuple of base classes instead of just one, and it will
    check whether `candidate` is a subclass of any of these base classes.
    
    This has the advantage that it doesn't throw an exception if `candidate` is
    not a type. (Python issue 10569.)        
    '''
    # todo: disable ability to use nested iterables.
    if cute_iter_tools.is_iterable(base_class):
        return any(is_subclass(candidate, single_base_class) for 
                   single_base_class in base_class)
    elif not isinstance(candidate, (type, types.ClassType)):
        return False
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
    return {name: _getattr(thing, name) for name in my_vars.iterkeys()}



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

        
class OwnNameDiscoveringDescriptor(object):
    '''A descriptor that can discover the name it's bound to on its object.'''
    
    def __init__(self, name=None):
        '''
        Construct the `OwnNameDiscoveringDescriptor`.
        
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
		

def find_clear_place_on_circle(circle_points, circle_size=1):
    '''
    Find the point on a circle that's the farthest away from other points.
    
    Given an interval `(0, circle_size)` and a bunch of points in it, find a
    place for a new point that is as far away from the other points as
    possible. (Since this is a circle, there's wraparound, e.g. the end of the
    interval connects to the start.)
    '''

    # Before starting, taking care of two edge cases:
    if not circle_points:
        # Edge case: No points at all
        return circle_size / 2
    if len(circle_points) == 1:
        # Edge case: Only one point
        return (circle_points[0] + circle_size / 2) % circle_size
    
    sorted_circle_points = sorted(circle_points)
    last_point = sorted_circle_points[-1]
    if last_point >= circle_size:
        raise Exception("One of the points (%s) is bigger than the circle "
                        "size %s." % (last_point, circle_size))
    clear_space = {}
    
    for first_point, second_point in \
        cute_iter_tools.iterate_overlapping_subsequences(sorted_circle_points,
                                                     wrap_around=True):
        
        clear_space[first_point] = second_point - first_point
        
    # That's the only one that might be negative, so we ensure it's positive:
    clear_space[last_point] %= circle_size
    
    maximum_clear_space = max(clear_space.itervalues())
    
    winners = [key for (key, value) in clear_space.iteritems()
               if value == maximum_clear_space]
    
    winner = winners[0]
    
    result = (winner + (maximum_clear_space / 2)) % circle_size
    
    return result
        
    
def add_extension_if_plain(path, extension):
    '''Add `extenstion` to a file path if it doesn't have an extenstion.'''
    
    if extension:
        assert extension.startswith('.')
    
    (without_extension, existing_extension) = os.path.splitext(path)
    if existing_extension:
        return path
    else: # not existing_extension
        return without_extension + extension
    
    
def general_sum(things, start=None):
    '''
    Sum a bunch of objects, adding them to each other.
    
    This is like the built-in `sum`, except it works for many types, not just
    numbers.
    '''
    if start is None:
        return reduce(operator.add, things)
    else:
        return reduce(operator.add, things, start)
    
    
def general_product(things, start=None):
    '''
    Multiply a bunch of objects by each other, not necessarily numbers.
    '''    
    if start is None:
        return reduce(operator.mul, things)
    else:
        return reduce(operator.mul, things, start)

    
def is_legal_email_address(email_address_candidate):
    '''Is `email_address_candidate` a legal email address?'''
    return bool(_email_pattern.match(email_address_candidate))


def is_type(thing):
    '''Is `thing` a class? Allowing both new-style and old-style classes.'''
    return isinstance(thing, (type, types.ClassType))

class NonInstatiable(object):
    '''
    Class that can't be instatiated.
    
    Inherit from this for classes that should never be instantiated, like
    constants and settings.
    '''
    def __new__(self, *args, **kwargs):
        raise RuntimeError('This class may not be instatiated.')    
    
def repeat_getattr(thing, query):
    '''
    Perform a repeated `getattr` operation.
    
    i.e., when given `repeat_getattr(x, '.y.z')`, will return `x.y.z`.
    '''
    if not query:
        return thing
    assert isinstance(query, str)
    if not query.startswith('.'):
        raise Exception('''`query` must start with '.', e.g. '.foo.bar.baz'.''')
    attribute_names = filter(None, query.split('.'))
    current = thing 
    for attribute_name in attribute_names:
        current = getattr(current, attribute_name)
    return current
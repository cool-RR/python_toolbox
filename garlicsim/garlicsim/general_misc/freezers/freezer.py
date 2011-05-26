# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `Freezer` class.

See its documentation for more information.
'''

from garlicsim.general_misc.third_party import abc

from garlicsim.general_misc import context_managers
from garlicsim.general_misc import proxy_property
from garlicsim.general_misc import caching

from .delegatee_context_manager import DelegateeContextManager


class Freezer(context_managers.DelegatingContextManager):
    '''
    A freezer is used as a context manager to "freeze" and "thaw" an object.
    
    Different kinds of objects have different concepts of "freezing" and
    "thawing": A GUI widget could be graphically frozen, preventing the OS from
    drawing any changes to it, and then when its thawed have all the changes
    drawn at once. As another example, an ORM could be frozen to have it not
    write to the database while a suite it being executed, and then have it
    write all the data at once when thawed.
    
    This class only implements the abstract behavior of a freezer: It is a
    reentrant context manager which has handlers for freezing and thawing, and
    its level of frozenness can be checked by accessing the attribute
    `.frozen`. It's up to subclasses to override `freeze_handler` and
    `thaw_handler` to do whatever they should do on freeze and thaw. Note that
    you can override either of these methods to be a no-op, sometimes even both
    methods, and still have a useful freezer by checking the property `.frozen`
    in the logic of the parent object.
    '''
    
    delegatee_context_manager = caching.CachedProperty(DelegateeContextManager)
    '''The context manager which implements our `__enter__` and `__exit__`.'''
    
    
    frozen = proxy_property.ProxyProperty('delegatee_context_manager.depth')
    '''
    An integer specifying the freezer's level of frozenness.
    
    If the freezer is not frozen, it's `0`. When it's frozen, it becomes `1`,
    and then every time the freezer is used as a context manager the `frozen`
    level increases. When reduced to `0` again the freezer is said to have
    thawed.
    
    This can be conveniently used as a boolean, i.e. `if my_freezer.frozen:`.
    '''
    
    
    @abc.abstractmethod
    def freeze_handler(self):
        '''Do something when the object gets frozen.'''
    
        
    @abc.abstractmethod
    def thaw_handler(self):
        '''Do something when the object gets thawed.'''
        
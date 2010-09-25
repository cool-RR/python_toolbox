# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

from garlicsim.general_misc.third_party import abc

# todo: can do __instancehook__ shit later

class BaseStepType(object): # todo: inherit from uninstanciable.
    # todo: should this be a metaclass?
    __metaclass__ = abc.ABCMeta
    
    # todo: this is enforcing only on instanciation, which doesn't help us.
    verbose_name = abc.abstractproperty()
    step_iterator_class = abc.abstractproperty()
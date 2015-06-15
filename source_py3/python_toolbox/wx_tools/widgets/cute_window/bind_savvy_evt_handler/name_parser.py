# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

import abc

from python_toolbox import abc_tools
from python_toolbox import sequence_tools
from python_toolbox import string_tools
from python_toolbox.misc_tools import name_mangling


class CaseStyleType(abc.ABCMeta):
    '''
    A type of case style, dictating in what convention names should be written.
    
    For example, `LowerCase` means names should be written 'like_this', while
    `CamelCase` means that names should be written 'LikeThis'.
    
    This is a metaclass; `LowerCase` and `CamelCase` are instances of this
    class.
    '''


class BaseCaseStyle(object):
    '''Base class for case styles.'''
    __metaclass__ = CaseStyleType
    
    @abc_tools.AbstractStaticMethod
    def parse(name):
        '''
        Parse a name with the given convention into a tuple of "words".
        
        Returns `None` if there is no match.
        '''
    
        
class LowerCase(BaseCaseStyle):
    '''Naming style specifying that names should be written 'like_this'.'''
    
    @staticmethod
    def parse(name):
        '''
        Parse a name with the given convention into a tuple of "words".
        
        For example, an input of 'on_navigation_panel__left_down' would result
        in an output of `('navigation_panel', 'left_down')`.
        
        Returns `None` if there is no match.
        '''
        if not name.startswith('on_'):
            return None
        cleaned_name = name[3:]
        words = tuple(cleaned_name.split('__'))
        return words

    
class CamelCase(BaseCaseStyle):
    '''Naming style specifying that names should be written 'LikeThis'.'''
    
    @staticmethod
    def parse(name):
        '''
        Parse a name with the given convention into a tuple of "words".
        
        For example, an input of 'OnNavigationPanel_LeftDown' would result in
        an output of `('navigation_panel', 'left_down')`.
        
        Returns `None` if there is no match.
        '''
        if not name.startswith('On'):
            return None
        cleaned_name = name[2:]
        words = tuple(cleaned_name.split('_'))
        return words


class NameParser(object):
    '''
    Parser that parses an event handler name.
    
    For example, under default settings, '_on_navigation_panel__left_down' will
    be parsed into a tuple `('navigation_panel', 'left_down')`.
    '''
    def __init__(self, case_style_possibilites=(LowerCase,),
                 n_preceding_underscores_possibilities=(1,)):
        '''
        Construct the `NameParser`.
        
        In `case_style_possibilites` you may specify a set of case styles
        (subclasses of `BaseCaseStyle`) that will be accepted by this parser.
        In `n_preceding_underscores_possibilities`, you may specify a set of
        ints signifying the number of underscores prefixing the name. For
        example, if you specify `(1, 2)`, this parser will accept names
        starting with either 1 or 2 underscores.
        '''
        
        self.case_style_possibilites = sequence_tools.to_tuple(
            case_style_possibilites,
            item_type=CaseStyleType
        )
        '''The set of case styles that this name parser accepts.'''
        
        self.n_preceding_underscores_possibilities = sequence_tools.to_tuple(
            n_preceding_underscores_possibilities
        )
        '''Set of number of preceding underscores that this parser accepts.'''
        
        
        assert all(isinstance(case_style, CaseStyleType) for case_style in 
                   self.case_style_possibilites)       
        assert all(isinstance(n_preceding_underscores, int) for
                   n_preceding_underscores in
                   self.n_preceding_underscores_possibilities)
        
                
    def parse(self, name, class_name):
        '''
        Parse a name into a tuple of "words".
        
        For example, under default settings, an input of
        '_on_navigation_panel__left_down' would result in an output of
        `('navigation_panel', 'left_down')`.
        
        Returns `None` if there is no match.
        '''
        unmangled_name = name_mangling.unmangle_attribute_name_if_needed(
            name,
            class_name
        )
        n_preceding_underscores = string_tools.get_n_identical_edge_characters(
            unmangled_name,
            character='_',
            head=True
        )
        if n_preceding_underscores not in \
           self.n_preceding_underscores_possibilities:
            return None
        cleaned_name = unmangled_name[n_preceding_underscores:]
        for case_style in self.case_style_possibilites:
            result = case_style.parse(cleaned_name)
            if result is not None:
                return result
        else:
            return None
    
        
    def match(self, name, class_name):
        '''Does `name` match our parser? (i.e. can it be parsed into words?)'''
        return (self.parse(name, class_name) is not None)
    
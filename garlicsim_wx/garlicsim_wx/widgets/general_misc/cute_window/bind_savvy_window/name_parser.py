# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `NameParser` class.

See its documentation for more information.
'''

from garlicsim.general_misc import sequence_tools
from garlicsim.general_misc import string_tools

class CaseStyleType(type):
    pass

class BaseCaseStyle(object):
    __metaclass__ = CaseStyleType
    
class LowerCase(BaseCaseStyle):
    @staticmethod
    def parse(name):
        if not name.startswith('on_'):
            return None
        cleaned_name = name[3:]
        words = cleaned_name.split('__')
        return words

class CamelCase(BaseCaseStyle):
    @staticmethod
    def parse(name):
        if not name.startswith('On'):
            return None
        cleaned_name = name[2:]
        raw_words = cleaned_name.split('_')
        words = map(string_tools.conversions.camelcase_to_underscore,
                    raw_words)
        return words


class NameParser(object):
    def __init__(self, case_style_possibilites=(LowerCase,),
                 n_preceding_underscores_possibilites=(1,)):
        
        self.case_style_possibilites = sequence_tools.to_tuple(
            case_style_possibilites,
            item_type=CaseStyleType
        )
        
        self.n_preceding_underscores_possibilites = sequence_tools.to_tuple(
            n_preceding_underscores_possibilites
        )
        
        
        assert all(isinstance(case_style, CaseStyleType) for case_style in 
                   self.case_style_possibilites)       
        assert all(isinstance(n_preceding_underscores, int) for
                   n_preceding_underscores in
                   self.n_preceding_underscores_possibilites)
        
                
    def parse(self, name):
        n_preceding_underscores = string_tools.get_n_identical_edge_characters(
            name,
            character='_',
            head=True
        )
        if n_preceding_underscores not in \
           self.n_preceding_underscores_possibilites:
            return None
        cleaned_name = name[n_preceding_underscores:]
        # blocktodo: What about the 'on' part?
        for case_style in self.case_style_possibilites:
            result = case_style.parse(cleaned_name)
            if result is not None:
                return result
        else:
            return None
    
        
    def match(self, name):
        return bool(self.parse(name))
    
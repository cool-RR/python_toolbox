from garlicsim.general_misc.third_party import inspect
from garlicsim.general_misc import cheat_hashing

from .sleek_ref import SleekRef
from .cute_sleek_value_dict import CuteSleekValueDict


__all__ = ['SleekCallArgs']

    
class SleekCallArgs(object):
    # What if we one of the args gets gc'ed before this SCA gets added to the
    # dictionary? It will render this SCA invalid, but we'll still be in the
    # dict. So make note to user: Always keep reference to args and kwargs until
    # the SCA gets added to the dict.
    def __init__(self, containing_dict, function, *args, **kwargs):
        
        self.containing_dict = containing_dict
        
        args_spec = inspect.getargspec(function)
        star_args_name, star_kwargs_name = \
                      args_spec.varargs, args_spec.keywords
        
        call_args = inspect.getcallargs(function, *args, **kwargs)
        del args, kwargs
        
        self.star_args_refs = []
        if star_args_name:
            star_args = call_args.pop(star_args_name, None)
            if star_args:
                self.star_args_refs = [SleekRef(star_arg, self.destroy) for
                                       star_arg in star_args]
        
        self.star_kwargs_refs = {}
        if star_kwargs_name:            
            star_kwargs = call_args.pop(star_kwargs_name, {})
            if star_kwargs:
                self.star_kwargs_refs = CuteSleekValueDict(self.destroy,
                                                                star_kwargs)
        
        self.args_refs = CuteSleekValueDict(self.destroy, call_args)
        
        # In the future the `.args`, `.star_args` and `.star_kwargs` attributes
        # may change, so we must record the hash now:
        self._hash = cheat_hashing.cheat_hash(
            (
                self.args,
                self.star_args,
                self.star_kwargs
            )
        )
        
        
    
    args = property(lambda self: dict(self.args_refs))
    
    star_args = property(
        lambda self:
            tuple((star_arg_ref() for star_arg_ref in self.star_args_refs))
    )
    
    star_kwargs = property(lambda self: dict(self.star_kwargs_refs))
    
        
    def destroy(self, _=None):
        if self.containing_dict:
            try:
                del self.containing_dict[self]
            except KeyError:
                pass
        
    
    def __hash__(self):
        return self._hash

    
    def __eq__(self, other):
        if not isinstance(other, SleekCallArgs):
            return NotImplemented
        return self.args == other.args and \
               self.star_args == other.star_args and \
               self.star_kwargs == other.star_kwargs
    
    
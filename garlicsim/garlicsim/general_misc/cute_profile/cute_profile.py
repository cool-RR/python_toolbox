import functools

from . import base_profile



def profile_ready(condition=None, off_after=True, sort=2):
    # todo: add condition option
    
    def decorator(function):
        
        def decorated(*args, **kwargs):
            
            if decorated.condition is not None:
                
                if decorated.condition is True or \
                   decorated.condition(decorated.original_function, *args,
                                       **kwargs):
                    
                    decorated.profiling_on = True
                    
            if decorated.profiling_on:
                
                if decorated.off_after:
                    decorated.profiling_on = False
                    decorated.condition = None
                    
                decorated.original_function # This line puts it in locals, weird
                
                base_profile.runctx(
                    'result = decorated.original_function(*args, **kwargs)',
                    globals(), locals(), sort=decorated.sort
                )                
                return locals()['result']
            
            else: # decorated.profiling_on is False
                
                return decorated.original_function(*args, **kwargs)
            
        decorated.original_function = function
        decorated.profiling_on = None
        decorated.condition = condition
        decorated.off_after = off_after
        decorated.sort = sort
        functools.update_wrapper(decorated, function)
        return decorated
    return decorator
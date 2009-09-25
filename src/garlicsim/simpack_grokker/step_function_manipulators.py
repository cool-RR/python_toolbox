def non_history_step_generator_from_simple_step(step_function, old_state,
                                                *args, **kwargs):
    current = old_state
    while True:
        current = step_function(current, *args, **kwargs)
        yield current
        
def history_step_generator_from_simple_step(step_function, history_browser,
                                            *args, **kwargs):
    while True:
        yield step_function(history_browser, *args, **kwargs)
        
def simple_non_history_step_from_step_generator(generator, history_browser,
                                                *args, **kwargs):
    iterator = generator(history_browser, *args, **kwargs)
    return iterator.next()

def simple_history_step_from_step_generator(generator, old_state,
                                            *args, **kwargs):
    iterator = generator(old_state, *args, **kwargs)
    return iterator.next()
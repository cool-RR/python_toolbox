from python_toolbox import misc_tools

from python_toolbox import emitting


def test():
    emitter_1 = emitting.Emitter()
    emitter_2 = emitting.Emitter(inputs=emitter_1) # Single item without tuple
    emitter_0 = emitting.Emitter(outputs=(emitter_1,))

    @misc_tools.set_attributes(call_counter=0)
    def my_function():
        my_function.call_counter += 1
    
    emitter_1.add_output(my_function)
    
    assert my_function.call_counter == 0
    emitter_1.emit()
    assert my_function.call_counter == 1
    emitter_1.emit()
    emitter_1.emit()
    emitter_1.emit()
    assert my_function.call_counter == 4
    emitter_0.emit()
    assert my_function.call_counter == 5
    emitter_0.emit()
    emitter_0.emit()
    emitter_0.emit()
    assert my_function.call_counter == 8
    emitter_2.emit()
    assert my_function.call_counter == 8
    emitter_2.emit()
    emitter_2.emit()
    emitter_2.emit()
    assert my_function.call_counter == 8



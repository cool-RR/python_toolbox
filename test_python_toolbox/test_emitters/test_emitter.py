from python_toolbox import emitters


def test():
    ''' '''
    emitter_1 = emitters.Emitter()
    emitter_2 = emitters.Emitter(inputs=(emitter_1,))
    emitter_0 = emitters.Emitter(outputs=(emitter_1,))

    def my_function():
        my_function.call_counter += 1
    my_function.call_counter = 0
    
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



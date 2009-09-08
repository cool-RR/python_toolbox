"""
A module that defines the `State` class. See
its documentation for more information.
"""



class State(object):
    """
    A State contains information about a
    "frozen moment" in the simulation.

    All the information about the state of the simulation should be saved in
    custom attributes of the State object.

    Most States are untouched, a.k.a. natural, but some States are touched.
    A touched State is a State that was not formed naturally by a simulation step:
    It was created by the user, either from scratch or based on another State.

    When a State is created, a ".clock" attribute must be assigned to it,
    specifying "what time it is" in this State.

    A State object must always be picklable, as do all the
    attributes assigned to it.
    """

    def __init__(self):
        pass

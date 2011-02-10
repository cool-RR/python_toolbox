'''

The reason it's important to test a simpack with a syntax error in its
`.settings` is because `SimpackGrokker` has some sensitive logic regarding
importing the `.settings` module. If one exists it should import it, and if one
doesn't it shouldn't, but if a `.settings` module exists and has a syntax error
it should propagate that error and not silence it.
'''

from .state import State
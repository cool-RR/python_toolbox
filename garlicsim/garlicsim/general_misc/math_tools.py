
def sign(x):
    if x > 0:
        return 1
    if x == 0:
        return 0
    assert x < 0
    return -1
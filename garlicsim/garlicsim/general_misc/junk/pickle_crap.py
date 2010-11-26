import pickle

class Object(object):
    pass

a = Object()
b = Object()

a.my_b = b
b.my_a = a

s = pickle.dumps(a)

0
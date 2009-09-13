import garlicsim.data_structures
import copy

import random
random.seed()

NUM_OF_BIOMORPH = 50
CITIES = [[89, 13], [33, 21], [39, 79], [57, 94], [13, 70], [88, 73], [12, 53], [25, 47], [92, 90], [1, 14]]
NUM_OF_CITIES = 10
MUTATION_RATE = 0.4

def make_random_state(*args,**kwargs):
    state=garlicsim.data_structures.State()
    state.freeze = 0
    state.min = 100000000
    state.biomorph = [];
    for i in range (NUM_OF_BIOMORPH):
        state.biomorph += [range(NUM_OF_CITIES)]
        random.shuffle(state.biomorph[i])

    return state

make_plain_state=make_random_state # Temporary

def step(source_state,*args,**kwargs):
    state=copy.deepcopy(source_state)
    state.clock+=1

    state.biomorph.sort(cmp_eval)
    if (evalF(state.biomorph[0]) == state.min):
        state.freeze+=1
    state.min = evalF(state.biomorph[0])
    if state.freeze == 25:
        for i in range(1,NUM_OF_BIOMORPH):
            random.shuffle(state.biomorph[i])
        state.freeze = 0
    else:
        for i in range(1,NUM_OF_BIOMORPH):
            state.biomorph[i] = merge(state.biomorph[i], state.biomorph[0])
    return state

def distance (a, b):
        return pow(pow(a[0]-b[0],2)+pow(a[1]-b[1],2),0.5)

def evalF (bio):
    result = 0
    for i in range(NUM_OF_CITIES-1):
        result += distance(CITIES[bio[i]], CITIES[bio[i+1]])
    return result



def cmp_eval(a,b):
    if ((evalF(a)-evalF(b)) > 0):
	return 1
    elif ((evalF(a)-evalF(b)) == 0):
	return 0
    else:
	return -1

def merge(a,b):
    if random.random() < 0.5:
        (a,b) = (b,a)
    p = random.randint(0,NUM_OF_CITIES)
    c=[]
    t= range(NUM_OF_CITIES)
    for i in range(NUM_OF_CITIES):
        if i < p:
            c += [a[i]]
            t.remove(a[i])
        else:
            for j in range(NUM_OF_CITIES):
                flag = 0
                for k in t:
                    if k == j:
                        flag = 1
                if flag == 1:
                    next = j
                    break
            c += [next]
            t.remove(next)
    while random.random() < MUTATION_RATE:
        r1 = random.choice(range(NUM_OF_CITIES))
        r2 = random.choice(range(NUM_OF_CITIES))
        (c[r1],c[r2]) = (c[r2],c[r1])
    return c






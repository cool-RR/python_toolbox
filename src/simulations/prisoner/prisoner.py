import state as state_module
import copy

import random
random.seed()


rounds=30


def make_random_state(*args,**kwargs):
    state=state_module.State()
    state._State__touched=True

    state.round=-1
    state.match=0

    state.player_pool=[random_strategy_player() for i in range(100)]

    return new_match_step(state)

def step(source_state,*args,**kwargs):
    state=copy.deepcopy(source_state)
    state._State__touched=False
    state.clock+=1

    state.round+=1
    if state.round==rounds:
        state.round=-1
        state.match+=1
        return new_match_step(state)

    for pair in state.pairs:
        play_game(pair,state.round)

    return state

def new_match_step(state):
    """
    Note: this function is not strictly a "step function":
    it manipulates the state that is given to it and then returns it.
    """
    state.pairs=pair_pool(state.player_pool)
    return state

def pair_pool(player_pool):
    """
    Takes a player pool and returns a list of random pairs of players.
    Every player will be a member of exactly one pair.
    """
    assert len(player_pool)%2==0
    result=[]
    pool=player_pool[:]
    while pool!=[]:
        pair=random.sample(pool,2)
        result.append(pair)

        pool.remove(pair[0])
        pool.remove(pair[1])
    return result

def play_game((x,y),round):
    x_move=x.play(round)
    y_move=y.play(round)

    assert x_move in ["Play nice","Play mean"]
    assert y_move in ["Play nice","Play mean"]

    if x_move=="Play nice" and y_move=="Play nice":
        x.points+= 1
        y.points+= 1
    elif x_move=="Play nice" and y_move=="Play mean":
        x.points+= -4
        y.points+= 2
    elif x_move=="Play mean" and y_move=="Play nice":
        x.points+= 2
        y.points+= -4
    elif x_move=="Play mean" and y_move=="Play mean":
        x.points+= -1
        y.points+= -1

    x.other_guy_played(y_move)
    y.other_guy_played(x_move)

def random_strategy_player():
    strategy=random.choice(strategies)
    return strategy()

class player(object):
    def __init__(self):
        self.points=0

    def play(self,*args,**kwargs):
        raise NotImplementedError

    def other_guy_played(self,move):
        pass

class angel(player):
    def play(self,round):
        return "Play nice"

class asshole(player):
    def play(self,round):
        return "Play mean"

class smarty(player):
    def play(self,round):
        if round==0:
            return "Play nice"
        else:
            return self.last_play

    def other_guy_played(self,move):
        self.last_play=move


strategies=[angel,asshole,smarty]







import garlicsim.data_structures
import garlicsim
import copy

import random
random.seed()


ROUNDS=7
NUMBER_OF_PLAYERS=70


BaseForHandicap = [object, garlicsim.PersistentReadOnlyObject] [1]

class Handicap(BaseForHandicap):
    def __init__(self, thing, meow):
        self.thing, self.meow = thing, meow
        self.big_list = [random.random() for i in range(100000)]

def make_plain_state(*args,**kwargs):
    global player_types
    state=garlicsim.data_structures.State()

    state.handicap = Handicap("The thing", meow="The meow")
    state.round=-1
    state.match=0

    state.player_pool=[player_types[i%len(player_types)]() for i in range(NUMBER_OF_PLAYERS)]

    return new_match_step(state)


def make_random_state(*args,**kwargs):
    state=garlicsim.data_structures.State()

    state.handicap = Handicap("The thing", meow="The meow")
    state.round=-1
    state.match=0

    state.player_pool=[random_strategy_player() for i in range(NUMBER_OF_PLAYERS)]

    return new_match_step(state)

def step(source_state,*args,**kwargs):
    state=copy.deepcopy(source_state)
    state.clock+=1

    state.round+=1
    if state.round==ROUNDS:
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
    pool=state.player_pool
    loser=player_with_least_points(pool)
    pool.remove(loser)
    pool.append(random_strategy_player())

    #for player in pool:
    #    player.points=0

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
    player=random.choice(player_types)
    return player()

class Player(object):
    def __init__(self):
        self.points=0

    def play(self,*args,**kwargs):
        raise NotImplementedError

    def other_guy_played(self,move):
        pass

class Angel(Player):
    def play(self,round):
        return "Play nice"

class Asshole(Player):
    def play(self,round):
        return "Play mean"

class Smarty(Player):
    def play(self,round):
        if round==0:
            return "Play nice"
        else:
            return self.last_play

    def other_guy_played(self,move):
        self.last_play=move


player_types=[Angel,Asshole,Smarty]

def how_many_players_of_certain_type(pool,type):
    n=0
    for player in pool:
        if isinstance(player,type):
            n+=1
    return n

def player_with_least_points(pool):
    assert len(pool)>0
    loser=pool[0]
    for player in pool:
        if player.points<loser.points:
            loser=player
    return loser









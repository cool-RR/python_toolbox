from __future__ import division

import os.path
import shutil
import tempfile
import re

from garlicsim.general_misc.temp_value_setters import \
    TempWorkingDirectorySetter
from garlicsim.general_misc import sys_tools
from garlicsim.general_misc import import_tools

import garlicsim.scripts.start_simpack
start_simpack_file = garlicsim.scripts.start_simpack.__file__

state_module_contents_for_coinflip = \
"""import random
import garlicsim.data_structures


class State(garlicsim.data_structures.State):

    def __init__(self, balance, last_bet_result=0):

        garlicsim.data_structures.State.__init__(self)

        self.balance = balance
        '''The current balance of our account, i.e. how much money we have.'''

        self.last_bet_result = last_bet_result
        '''How much we won/lost in the last bet. `-100` means we lost $100.'''


    def step(self):

        if self.balance >= 6000:
            raise garlicsim.misc.WorldEnd

        # First we need to calculate how much we're going to bet in this round.

        if self.last_bet_result >= 0:
            # Meaning either (1) we just started the simulation or (2) we
            # just won $100.
            amount_to_bet = 100 # We're starting a new cycle

        else:
            # If the flow reached here it means we just lost. So we
            # should bet double the amount:
            amount_to_bet = - 2 * self.last_bet_result

        if amount_to_bet > self.balance:
            # If we don't have the amount we should bet, we stop the simulation.
            # True, we can try to bet whatever's left, but for simplicity's sake
            # we won't do that now.
            raise garlicsim.misc.WorldEnd

        # Let's bet!
        bet_result = random.choice([amount_to_bet, - amount_to_bet])

        new_balance = self.balance + bet_result

        new_state = State(new_balance, bet_result)

        return new_state


    @staticmethod
    def create_root():
        return State(balance=5000)"""

def test():
    # tododoc: do this. Don't forget to test the simpack works.
    
    # Asserting we don't have a `_coin_flip` on path already in some other
    # place:
    assert not import_tools.exists('_coin_flip')
    
    temp_dir = tempfile.mkdtemp(prefix='temp_garlicsim_')
    try:
        with TempWorkingDirectorySetter(temp_dir):
            with sys_tools.OutputCapturer() as output_capturer:
                garlicsim.scripts.start_simpack.execute(
                    argv=['start_simpack.py', '_coin_flip']
                )
            assert output_capturer.output == \
                ("`_coin_flip` simpack created successfully! Explore the "
                 "`_coin_flip` folder and start filling in the contents of "
                 "your new simpack.\n")
            simpack_path = os.path.join(temp_dir, '_coin_flip')
            assert os.path.isdir(simpack_path)
            state_module_path = os.path.join(simpack_path, 'state.py')
            with open(state_module_path, 'w') as state_file:
                state_file.write(state_module_contents_for_coinflip)
                
             
            #string_to_replace = re.search(
                #'    # This is your State subclass.*$',
                #state_file_contents
            #)
            #state_file_contents.replace(
                #string_to_replace,
                
            #)
            #fixed_state_file_contents = state_file_contents.replace('''\
            
            #)
            #with open(state_module_path, 'r') as state_file_for_reading:
            
            with sys_tools.TempSysPathAdder(temp_dir):
                import _coin_flip
                state = _coin_flip.State.create_root()
                assert repr(vars(state)) == \
                       "{'balance': 5000, 'last_bet_result': 0}"

                new_state = garlicsim.simulate(state, 5)
                assert repr(vars(new_state)) == \
                "{'balance': %s, 'clock': %s, 'last_bet_result': %s}" % \
                (new_state.balance, new_state.clock, new_state.last_bet_result)
                
                from garlicsim.general_misc.infinity import Infinity
                
                got_winner = False
                got_loser = False
                while not (got_winner and got_loser):
                    new_state = garlicsim.simulate(state, Infinity)
                    assert repr(vars(new_state)) == \
                           ("{'balance': %s, 'clock': %s, 'last_bet_result': "
                            "%s}" % (new_state.balance, new_state.clock,
                            new_state.last_bet_result))
                    assert new_state.balance <= 6000
                    if new_state.balance == 6000:
                        got_winner = True
                        continue
                    else:
                        assert new_state.last_bet_result < 0
                        assert new_state.balance <= \
                            (-2) * new_state.last_bet_result
                        got_loser = True
                        continue
            
            
            
    finally:
        shutil.rmtree(temp_dir)

        
def test_implicit_help():
    pass#tododoc
        

def test_explicit_help():
    pass#tododoc
    
import random
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
            raise garlicsim.misc.exceptions.WorldEnd
        
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
            raise garlicsim.misc.exceptions.WorldEnd
            
        # Let's bet!
        bet_result = random.choice([amount_to_bet, - amount_to_bet])
        
        new_balance = self.balance + bet_result
        
        new_state = State(new_balance, bet_result)
        
        return new_state
    
        
    @staticmethod
    def create_root():
        return State(balance=5000)

    
    

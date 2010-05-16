import random
import garlicsim.data_structures

class State(garlicsim.data_structures.State):
    # This is your State subclass. Your state objects should contain all the
    # information there is about a moment of time in your simulation.
    
    def __init__(self, balance, last_bet_result=0):
        
        garlicsim.data_structures.State.__init__(self)
        
        self.balance = balance
        '''The current balance of our account, i.e. how much money we have.'''
        
        if self.balance >= 6000:
            self.end_result = 6000
            # If we reach 6,000, we won.
        
        self.last_bet_result = last_bet_result
        '''How much we won/lost in the last bet. `-100` means we lost $100.'''
        
        self.calculate_amount_to_bet()
    
        
    def calculate_amount_to_bet(self):
        # This method calculates how much we should bet in this round, and
        # places that amount as an attribute `.amount_to_bet`
        
        if self.last_bet_result >= 0:
            # Meaning either (1) we just started the simulation or (2) we
            # just won $100.                
            amount_to_bet = 100 # We're starting a new cycle
            
        else: 
            # If the flow reached here it means we just lost. So we
            # should bet double the amount:
            amount_to_bet = - 2 * self.last_bet_result
        
            
        self.amount_to_bet = amount_to_bet
        
        # Now we know what the amount we should bet. Let's make sure we have it:
        
        if amount_to_bet > self.balance: # If we don't have it
            self.end_result = self.balance # Then we just stop betting
        
        
    def step(self):
        
        # Let's bet!
        bet_result = random.choice([self.amount_to_bet, - self.amount_to_bet])
        
        new_balance = self.balance + bet_result
        
        new_state = State(new_balance, bet_result)
        
        return new_state
    
        
    @staticmethod
    def create_root():
        return State(balance=5000)

    
    

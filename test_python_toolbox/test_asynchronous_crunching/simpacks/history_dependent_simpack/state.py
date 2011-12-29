from garlicsim.general_misc.infinity import infinity
from garlicsim.general_misc import binary_search

import garlicsim.data_structures


class State(garlicsim.data_structures.State):
    
    def __init__(self):
        pass
    
    @staticmethod
    def history_step(history_browser):
        assert isinstance(
            history_browser,
            garlicsim.misc.base_history_browser.BaseHistoryBrowser
        )
        first_state = history_browser[0]
        last_state = history_browser[-1]
        assert last_state is history_browser.get_last_state()
        n_states = len(history_browser)
        # todo: If ever doing `BaseHistoryBrowser.__iter__`, should test it here
        # and compare to other methods.
        assert last_state is history_browser[n_states - 1]
        assert first_state is history_browser[-n_states]
        if n_states >= 2:
            second_state = history_browser[1]
            second_to_last_state = history_browser[-2]
            assert second_state is history_browser[- n_states + 1]
            assert second_to_last_state is history_browser[n_states - 2]
            if n_states >= 3:
                assert first_state.clock < second_state.clock <= \
                       second_to_last_state.clock < last_state.clock
            
        assert history_browser.get_state_by_clock(-infinity) is first_state
        assert history_browser.get_state_by_clock(infinity) is last_state
        
        assert history_browser.get_state_by_clock(
            -infinity,
            binary_search.roundings.BOTH
        ) == (None, first_state)
        assert history_browser.get_state_by_clock(
            infinity,
            binary_search.roundings.BOTH
        ) == (last_state, None)
        
            
        
        return State()
        
    @staticmethod
    def create_root():
        return State()
    
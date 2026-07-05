# -*- coding: utf-8 -*-
from turing_machine import TuringMachine
from test_turing_machine_example1 import print_states

transitions = {
    ('a', '0'): ('b', '1', 'R'),
    ('a', '1'): ('b', '1', 'L'),
    ('b', '0'): ('a', '1', 'L'),
    ('b', '1'): ('qa', '1', 'R'),
}

if __name__ == "__main__":
    print_states(transitions)
    tm = TuringMachine(
        transitions,
        start_state='a',
        accept_state='qa',
        reject_state='r',
        blank_symbol='0'        
    )
    print("================")
    print("BB with 2 states")
    tm.debug("", step_limit=50) 
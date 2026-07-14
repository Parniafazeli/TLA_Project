from turing_machine import TuringMachine
from test_turing_machine_example1 import print_states

transitions = {
    ('a', '0'): ('b', '1', 'R'),
    ('a', '1'): ('c', '1', 'L'),
    ('b', '0'): ('a', '1', 'L'),
    ('b', '1'): ('b', '1', 'R'),
    ('c', '0'): ('b', '1', 'L'),
    ('c', '1'): ('h', '1', 'R'),
}

if __name__ == "__main__":
    print("================")
    print("BB with 3 states")
    print_states(transitions)
    tm = TuringMachine(
        transitions,
        start_state='a',
        accept_state='h',
        reject_state='r',
        blank_symbol='0'        
    )
    tm.debug("", step_limit=200)
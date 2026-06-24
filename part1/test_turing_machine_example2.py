from turing_machine import TuringMachine
from test_turing_machine_example1 import print_states

transitions = {
    ('q0', '#'): ('End', '#', 'R'),
    ('End', ''): ('qa', '', 'R'),

    ('q0', '0'): ('FindDelimiter0', 'X', 'R'),
    ('FindDelimiter0', '#'): ('Check0', '#', 'R'),
    ('Check0', '0'): ('FindLeftmost', 'X', 'L'),

    ('q0', '1'): ('FindDelimiter1', 'X', 'R'),
    ('FindDelimiter1', '#'): ('Check1', '#', 'R'),
    ('Check1', '1'): ('FindLeftmost', 'X', 'L'),

    ('FindLeftmost', '0'): ('FindLeftmost', '0', 'L'),
    ('FindLeftmost', '1'): ('FindLeftmost', '1', 'L'),
    ('FindLeftmost', 'X'): ('FindLeftmost', 'X', 'L'),
    ('FindLeftmost', '#'): ('FindLeftmost', '#', 'L'),
    ('FindLeftmost', ''): ('FindNext', '', 'R'),

    ('FindNext', 'X'): ('FindNext', 'X', 'R'),
    ('FindNext', '0'): ('FindDelimiter0', 'X', 'R'),
    ('FindNext', '1'): ('FindDelimiter1', 'X', 'R'),
    ('FindNext', '#'): ('End', '#', 'R'),

    ('FindDelimiter0', '0'): ('FindDelimiter0', '0', 'R'),
    ('FindDelimiter0', '1'): ('FindDelimiter0', '1', 'R'),
    ('FindDelimiter1', '0'): ('FindDelimiter1', '0', 'R'),
    ('FindDelimiter1', '1'): ('FindDelimiter1', '1', 'R'),

    ('Check0', 'X'): ('Check0', 'X', 'R'),
    ('Check1', 'X'): ('Check1', 'X', 'R'),

    ('End', 'X'): ('End', 'X', 'R')
}

def run(input_):
    machine = TuringMachine(transitions)
    print("Input:", input_)
    for action, config in machine.run(input_):
        left = ''.join(reversed(config['left_hand_side']))
        right = ''.join(config['right_hand_side'])
        print(f"{config['state']} {left}[{config['symbol']}]{right}")
        if action is not None:
            print(f"Halts with {action}")
            break
    print()

if __name__ == "__main__":
    print_states(transitions)

    # ACCEPTS
    run("#")
    run("0#XXXX0")
    run("1#XXXX1")
    run("11#XXXX11")
    run("01#XXXX01")
    run("01#01")
    run("101#101")

    # REJECTS
    run("0000#XXXX1")
    run("0111#XXXX1")
    run("0111#XXXX0")
    run("11#XXXX1")
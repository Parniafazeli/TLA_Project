from turing_machine import TuringMachine

transitions = {
    ('q0', '#'): ('saw_#', '#', 'R'),
    ('saw_#', '#'): ('saw_##', '#', 'R'),
    ('saw_##', ''): ('qa', '', 'R'),
}

def print_states(transition_mapping):
    states = set()
    for (start, finish) in transition_mapping.items():
        (s1, _) = start
        (s2, _, _) = finish
        states.add(s1)
        states.add(s2)
    states.add('qa')  # accept state
    print("The Turing machine has", len(states), "states:")
    for i in sorted(states):
        print(i)
    print()

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

    # SHOULD ACCEPT
    run("##")

    # SHOULD REJECT
    run("101031##")
    run("######")
    run("#####")
    run("#_#_")
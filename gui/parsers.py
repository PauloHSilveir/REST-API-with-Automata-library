# filepath: /home/paulo/Documentos/REST-API-with-Automata-library/parsers.py
def parse_transitions_dfa(transitions_str):
    transitions = {}
    lines = transitions_str.strip().split("\n")
    for line in lines:
        parts = line.split(",")
        if len(parts) != 3:
            raise ValueError(f"Invalid transition format: {line}")
        state, symbol, next_state = parts
        state = state.strip()
        symbol = symbol.strip()
        next_state = next_state.strip()
        if state not in transitions:
            transitions[state] = {}
        transitions[state][symbol] = next_state
    return transitions

def parse_transitions_dpda(transitions_str):
    transitions = {}
    lines = transitions_str.strip().split("\n")
    for line in lines:
        parts = line.split(",")
        if len(parts) != 5:
            raise ValueError(f"Invalid transition format: {line}")
        state, symbol, stack_symbol, next_state, stack_action = parts
        state = state.strip()
        symbol = symbol.strip()
        stack_symbol = stack_symbol.strip()
        next_state = next_state.strip()
        stack_action = stack_action.strip()
        if state not in transitions:
            transitions[state] = {}
        if symbol not in transitions[state]:
            transitions[state][symbol] = {}
        transitions[state][symbol][stack_symbol] = [next_state, stack_action.split()]
    return transitions

def parse_transitions_ntm(transitions_str):
    transitions = {}
    lines = transitions_str.strip().split("\n")
    for line in lines:
        parts = line.split(",")
        if len(parts) != 5:
            raise ValueError(f"Invalid transition format: {line}")
        state, symbol, next_state, write_symbol, direction = parts
        state = state.strip()
        symbol = symbol.strip()
        next_state = next_state.strip()
        write_symbol = write_symbol.strip()
        direction = direction.strip()
        if state not in transitions:
            transitions[state] = {}
        if symbol not in transitions[state]:
            transitions[state][symbol] = []
        transitions[state][symbol].append([next_state, write_symbol, direction])
    return transitions
# filepath: /home/paulo/Documentos/REST-API-with-Automata-library/submitters.py
import requests
from tkinter import messagebox
from gui.parsers import parse_transitions_dfa, parse_transitions_dpda, parse_transitions_ntm

def submit_dfa(entry_states, entry_input_symbols, entry_transitions, entry_initial_state, entry_final_states):
    states = entry_states.get().split(",")
    input_symbols = entry_input_symbols.get().split(",")
    transitions_str = entry_transitions.get("1.0", "end")
    transitions = parse_transitions_dfa(transitions_str)
    initial_state = entry_initial_state.get()
    final_states = entry_final_states.get().split(",")

    dfa_data = {
        "states": states,
        "input_symbols": input_symbols,
        "transitions": transitions,
        "initial_state": initial_state,
        "final_states": final_states
    }

    response = requests.post("http://localhost:8000/dfa/", json=dfa_data)
    if response.status_code == 200:
        messagebox.showinfo("Success", "DFA created successfully!")
    else:
        messagebox.showerror("Error", "Failed to create DFA")

def submit_dpda(entry_states, entry_input_symbols, entry_stack_symbols, entry_transitions, entry_initial_state, entry_initial_stack_symbol, entry_final_states, entry_acceptance_mode):
    states = entry_states.get().split(",")
    input_symbols = entry_input_symbols.get().split(",")
    stack_symbols = entry_stack_symbols.get().split(",")
    transitions_str = entry_transitions.get("1.0", "end")
    transitions = parse_transitions_dpda(transitions_str)
    initial_state = entry_initial_state.get()
    initial_stack_symbol = entry_initial_stack_symbol.get()
    final_states = entry_final_states.get().split(",")
    acceptance_mode = entry_acceptance_mode.get()

    dpda_data = {
        "states": states,
        "input_symbols": input_symbols,
        "stack_symbols": stack_symbols,
        "transitions": transitions,
        "initial_state": initial_state,
        "initial_stack_symbol": initial_stack_symbol,
        "final_states": final_states,
        "acceptance_mode": acceptance_mode
    }

    response = requests.post("http://localhost:8000/dpda/", json=dpda_data)
    if response.status_code == 200:
        messagebox.showinfo("Success", "DPDA created successfully!")
    else:
        messagebox.showerror("Error", "Failed to create DPDA")

def submit_ntm(entry_states, entry_input_symbols, entry_tape_symbols, entry_transitions, entry_initial_state, entry_blank_symbol, entry_final_states, entry_valid_directions):
    states = entry_states.get().split(",")
    input_symbols = entry_input_symbols.get().split(",")
    tape_symbols = entry_tape_symbols.get().split(",")
    transitions_str = entry_transitions.get("1.0", "end")
    transitions = parse_transitions_ntm(transitions_str)
    initial_state = entry_initial_state.get()
    blank_symbol = entry_blank_symbol.get()
    final_states = entry_final_states.get().split(",")
    valid_directions = entry_valid_directions.get().split(",")

    ntm_data = {
        "states": states,
        "input_symbols": input_symbols,
        "tape_symbols": tape_symbols,
        "transitions": transitions,
        "initial_state": initial_state,
        "blank_symbol": blank_symbol,
        "final_states": final_states,
        "valid_directions": valid_directions
    }

    response = requests.post("http://localhost:8000/ntm/", json=ntm_data)
    if response.status_code == 200:
        messagebox.showinfo("Success", "NTM created successfully!")
    else:
        messagebox.showerror("Error", "Failed to create NTM")
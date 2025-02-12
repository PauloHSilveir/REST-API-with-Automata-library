# filepath: /home/paulo/Documentos/REST-API-with-Automata-library/menu.py
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import json
import io
from gui.submitters import submit_dfa, submit_dpda, submit_ntm

def get_automaton_image():
    automaton_id = entry_automaton_id.get()

    response = requests.get(f"http://localhost:8000/automaton_image/{automaton_id}")
    if response.status_code == 200:
        image_data = response.content
        image = Image.open(io.BytesIO(image_data))
        image = ImageTk.PhotoImage(image)
        image_label.config(image=image)
        image_label.image = image
    else:
        messagebox.showerror("Error", "Failed to retrieve automaton image")

def get_automaton_info():
    automaton_id = entry_automaton_id.get()
    response = requests.get(f"http://localhost:8000/ntm/{automaton_id}")
    if response.status_code == 404:
        response = requests.get(f"http://localhost:8000/dfa/{automaton_id}")
    if response.status_code == 404:
        response = requests.get(f"http://localhost:8000/dpda/{automaton_id}")
    if response.status_code == 200:
        automaton_data = response.json()
        info_text.delete("1.0", tk.END)
        info_text.insert(tk.END, json.dumps(automaton_data, indent=4))
    else:
        messagebox.showerror("Error", "Failed to retrieve automaton information")

def test_automaton():
    automaton_id = entry_automaton_id.get()
    input_str = entry_input_string.get()

    try:
        response = requests.post(f"http://localhost:8000/validate_input/{automaton_id}", json={"input_str": input_str})

        if response.status_code == 200:
            result = response.json()
            print(result)   
            if result["accepted"]:
                messagebox.showinfo("Success", f"The input string '{input_str}' is accepted by the automaton!")
            else:
                messagebox.showinfo("Failure", f"The input string '{input_str}' is not accepted by the automaton.")
        else:
            messagebox.showerror("Error", f"Failed to test input automaton: {response.text}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Request failed: {e}")

def show_main_menu():
    for widget in root.winfo_children():
        widget.destroy()
    main_menu()

def show_create_automaton():
    for widget in root.winfo_children():
        widget.destroy()
    create_automaton_interface()

def show_view_automaton():
    for widget in root.winfo_children():
        widget.destroy()
    view_automaton_interface()

def show_view_automaton_info():
    for widget in root.winfo_children():
        widget.destroy()
    view_automaton_info_interface()

def show_test_automaton():
    for widget in root.winfo_children():
        widget.destroy()
    test_automaton_interface()

def create_automaton_interface():
    tk.Label(root, text="States (comma-separated):").grid(row=0, column=0)
    global entry_states
    entry_states = tk.Entry(root)
    entry_states.grid(row=0, column=1)

    tk.Label(root, text="Input Symbols (comma-separated):").grid(row=1, column=0)
    global entry_input_symbols
    entry_input_symbols = tk.Entry(root)
    entry_input_symbols.grid(row=1, column=1)

    tk.Label(root, text="Stack Symbols (comma-separated):").grid(row=2, column=0)
    global entry_stack_symbols
    entry_stack_symbols = tk.Entry(root)
    entry_stack_symbols.grid(row=2, column=1)

    tk.Label(root, text="Tape Symbols (comma-separated):").grid(row=3, column=0)
    global entry_tape_symbols
    entry_tape_symbols = tk.Entry(root)
    entry_tape_symbols.grid(row=3, column=1)

    tk.Label(root, text="Transitions (one per line):").grid(row=4, column=0)
    global entry_transitions
    entry_transitions = tk.Text(root, height=10, width=50)
    entry_transitions.grid(row=4, column=1)

    tk.Label(root, text="Initial State:").grid(row=5, column=0)
    global entry_initial_state
    entry_initial_state = tk.Entry(root)
    entry_initial_state.grid(row=5, column=1)

    tk.Label(root, text="Initial Stack Symbol:").grid(row=6, column=0)
    global entry_initial_stack_symbol
    entry_initial_stack_symbol = tk.Entry(root)
    entry_initial_stack_symbol.grid(row=6, column=1)

    tk.Label(root, text="Blank Symbol:").grid(row=7, column=0)
    global entry_blank_symbol
    entry_blank_symbol = tk.Entry(root)
    entry_blank_symbol.grid(row=7, column=1)

    tk.Label(root, text="Final States (comma-separated):").grid(row=8, column=0)
    global entry_final_states
    entry_final_states = tk.Entry(root)
    entry_final_states.grid(row=8, column=1)

    tk.Label(root, text="Valid Directions (comma-separated):").grid(row=9, column=0)
    global entry_valid_directions
    entry_valid_directions = tk.Entry(root)
    entry_valid_directions.grid(row=9, column=1)

    tk.Label(root, text="Acceptance Mode:").grid(row=10, column=0)
    global entry_acceptance_mode
    entry_acceptance_mode = tk.Entry(root)
    entry_acceptance_mode.grid(row=10, column=1)

    tk.Button(root, text="Submit DFA", command=submit_dfa).grid(row=11, column=0)
    tk.Button(root, text="Submit DPDA", command=submit_dpda).grid(row=11, column=1)
    tk.Button(root, text="Submit NTM", command=submit_ntm).grid(row=11, column=2)
    tk.Button(root, text="Back", command=show_main_menu).grid(row=12, column=1)

def view_automaton_interface():
    tk.Label(root, text="Automaton ID:").grid(row=0, column=0)
    global entry_automaton_id
    entry_automaton_id = tk.Entry(root)
    entry_automaton_id.grid(row=0, column=1)

    tk.Button(root, text="Get Automaton Image", command=get_automaton_image).grid(row=0, column=2)

    global image_label
    image_label = tk.Label(root)
    image_label.grid(row=1, column=0, columnspan=3)

    tk.Button(root, text="Back", command=show_main_menu).grid(row=2, column=1)

def view_automaton_info_interface():
    tk.Label(root, text="Automaton ID:").grid(row=0, column=0)
    global entry_automaton_id
    entry_automaton_id = tk.Entry(root)
    entry_automaton_id.grid(row=0, column=1)

    tk.Button(root, text="Get Automaton Info", command=get_automaton_info).grid(row=0, column=2)

    global info_text
    info_text = tk.Text(root, height=20, width=80)
    info_text.grid(row=1, column=0, columnspan=3)

    tk.Button(root, text="Back", command=show_main_menu).grid(row=2, column=1)

def test_automaton_interface():
    tk.Label(root, text="Automaton ID:").grid(row=0, column=0)
    global entry_automaton_id
    entry_automaton_id = tk.Entry(root)
    entry_automaton_id.grid(row=0, column=1)

    tk.Label(root, text="Input String:").grid(row=1, column=0)
    global entry_input_string
    entry_input_string = tk.Entry(root)
    entry_input_string.grid(row=1, column=1)

    tk.Button(root, text="Test Input", command=test_automaton).grid(row=2, column=0)

    tk.Button(root, text="Back", command=show_main_menu).grid(row=2, column=1)

def main_menu():
    tk.Button(root, text="Create Automaton", command=show_create_automaton).pack(pady=10)
    tk.Button(root, text="View Automaton", command=show_view_automaton).pack(pady=10)
    tk.Button(root, text="Test Automaton", command=show_test_automaton).pack(pady=10)
    tk.Button(root, text="View Automaton Info", command=show_view_automaton_info).pack(pady=10)

root = tk.Tk()
root.title("Automaton Creator")

main_menu()

root.mainloop()
from typing import Union

from fastapi import FastAPI
from Item import Item
from NTMModel import NTMModel  # Import NTMModel
from automato.ntm_visualizer import draw_ntm, load_automaton
from automata.fa.dfa import DFA


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

@app.post("/ntm/")
async def receive_ntm(ntm: NTMModel):
    return {
        "message": "NTM received successfully", 
        "data": ntm

    }

@app.get("/generate_automaton/")
def generate_automaton():
    automaton = load_automaton("data/automato.json")
    draw_ntm(automaton, "output/automato.png")
    return {"message": "Automaton image generated"}

def read_user_input(my_automaton):
    try:
        while True:
            if my_automaton.accepts_input(input("Please enter your input: ")):
                print("Accepted")
            else:
                print("Rejected")
    except KeyboardInterrupt:
        print("")


# DFA which matches all binary strings ending in an odd number of '1's
my_dfa = DFA(
    states={'q0', 'q1', 'q2'},
    input_symbols={'0', '1'},
    transitions={
        'q0': {'0': 'q0', '1': 'q1'},
        'q1': {'0': 'q0', '1': 'q2'},
        'q2': {'0': 'q2', '1': 'q1'}
    },
    initial_state='q0',
    final_states={'q1'}
)


read_user_input(my_dfa)
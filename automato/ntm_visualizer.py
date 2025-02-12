import json
import os
from graphviz import Digraph

def load_automaton(json_path: str):
    """Carrega a definição do autômato a partir de um arquivo JSON."""
    with open(json_path, 'r') as f:
        return json.load(f)

def draw_ntm(automaton, output_path="automato.png"):
    """Gera e salva um diagrama do autômato."""
    dot = Digraph(format="png")

    # Adiciona os estados
    for state in automaton["states"]:
        shape = "doublecircle" if state in automaton["final_states"] else "circle"
        dot.node(state, shape=shape)

    # Adiciona as transições
    for state, transitions in automaton["transitions"].items():
        for symbol, actions in transitions.items():
            for next_state, write_symbol, direction in actions:
                label = f"{symbol} → {write_symbol}, {direction}"
                dot.edge(state, next_state, label=label)

    # Define o estado inicial
    dot.node("start", shape="none", label="")
    dot.edge("start", automaton["initial_state"])

    # Salva o gráfico
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)
    dot.render(output_path.replace(".png", ""))

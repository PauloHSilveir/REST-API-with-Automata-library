# filepath: /home/paulo/Documentos/REST-API-with-Automata-library/automato/dfa_visualizer.py
from graphviz import Digraph

def draw_dfa(dfa_data, output_path):
    dot = Digraph()

    # Adiciona os estados
    for state in dfa_data["states"]:
        if state in dfa_data["final_states"]:
            dot.node(state, shape="doublecircle")
        else:
            dot.node(state, shape="circle")

    # Adiciona as transições
    for state, transitions in dfa_data["transitions"].items():
        for symbol, next_state in transitions.items():
            dot.edge(state, next_state, label=symbol)

    # Adiciona o estado inicial
    dot.node("", shape="none", width="0", height="0")
    dot.edge("", dfa_data["initial_state"])

    # Salva o arquivo
    dot.render(output_path, format="png", cleanup=True)
# filepath: /home/paulo/Documentos/REST-API-with-Automata-library/automato/dpda_visualizer.py
from graphviz import Digraph

def draw_dpda(dpda_data, output_path):
    dot = Digraph()

    # Adiciona os estados
    for state in dpda_data["states"]:
        if state in dpda_data["final_states"]:
            dot.node(state, shape="doublecircle")
        else:
            dot.node(state, shape="circle")

    # Adiciona as transições
    for state, transitions in dpda_data["transitions"].items():
        for symbol, stack_transitions in transitions.items():
            for stack_symbol, (next_state, stack_action) in stack_transitions.items():
                label = f"{symbol}, {stack_symbol} -> {stack_action}"
                dot.edge(state, next_state, label=label)

    # Adiciona o estado inicial
    dot.node("", shape="none", width="0", height="0")
    dot.edge("", dpda_data["initial_state"])

    # Salva o arquivo
    dot.render(output_path, format="png", cleanup=True)
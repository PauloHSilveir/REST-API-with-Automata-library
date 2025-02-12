# filepath: /home/paulo/Documentos/REST-API-with-Automata-library/visualizers.py
from automato.ntm_visualizer import draw_ntm
from automato.dfa_visualizer import draw_dfa
from automato.dpda_visualizer import draw_dpda

OUTPUT_DIR = "output"

def generate_automaton_image(automaton, automaton_id):
    if "tape_symbols" in automaton:
        draw_ntm(automaton, f"{OUTPUT_DIR}/{automaton_id}.png")
    elif "stack_symbols" in automaton:
        draw_dpda(automaton, f"{OUTPUT_DIR}/{automaton_id}.png")
    else:
        draw_dfa(automaton, f"{OUTPUT_DIR}/{automaton_id}.png")
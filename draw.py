"""
Function to draw the automaton. Taken from the first exercise,
modified to comply with pylint rules.
"""

import graphviz

def draw_automaton(aut):
    """
    Function to draw the automaton.
    """
    graph = graphviz.Digraph('Automaton')

    for state in aut.states:
        if state in aut.final_states:
            graph.attr('node', style='bold')
        if state == aut.initial_state:
            graph.node(str(state), label="-> " + str(state))
        else:
            graph.node(str(state))
        graph.attr('node', style='solid')

    for x_var, label, z_var in aut.delta:
        graph.edge(str(x_var), str(z_var), label=" " + label + " ")

    return graph

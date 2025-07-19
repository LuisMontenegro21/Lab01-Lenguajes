from graphviz import Digraph


def visualize_automaton(automata: object) -> None:
    dot = Digraph()
    dot.attr(rankir='LR')

    dot.node('', shape='none')
    dot.edge('', f'q{automata.initial_state}')

    for state in automata.states:
        shape = 'doublecircle' if state in automata.final_states else 'circle'
        dot.node(f'q{state}', shape=shape)
    
    for src, edges in automata.transitions.items():
        for symbol, dst in edges.items():
            dot.edge(f'q{src}', f'q{dst}', label=symbol)
    filename: str = automata.__qualname__
    dot.render(f"Images/{filename}", format='png', cleanup=True)
    
import networkx as nx
import matplotlib.pyplot as plt


def visualize_automaton(automata: object) -> None:
    G = nx.DiGraph()
    initial = f'q{automata.initial_state}'

    for state in automata.states:
        node_label = f'q{state}'
        G.add_node(node_label, is_final=state in automata.final_states)
    
    G.add_node('start', shape='none')
    G.add_edge('start', initial, label='')

    for src, edges in automata.transitions.items():
        for symbol, dst in edges.items():
            src_label = f'q{src}'
            dst_label = f'q{dst}'
            G.add_edge(src_label, dst_label, label=symbol)
    
    pos = nx.spring_layout(G, seed=42)
    final_nodes = [n for n, d in G.nodes(data=True) if d.get("is_final")]
    other_nodes = [n for n in G.nodes() if n not in final_nodes and n != 'start']

    nx.draw_networkx_nodes(G, pos, nodelist=other_nodes, node_color='skyblue', node_size=1500)
    nx.draw_networkx_nodes(G, pos, nodelist=final_nodes, node_color='lightgreen', node_shape='o', node_size=1500)
    nx.draw_networkx_nodes(G, pos, nodelist=['start'], node_color='white', node_shape='o', node_size=1)

    nx.draw_networkx_edges(G, pos, arrows=True, arrowstyle='->', connectionstyle='arc3,rad=0.1')


    nx.draw_networkx_labels(G, pos, font_size=12)
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)

    plt.axis('off')
    filename:str = automata.get_name()
    plt.title(f"Automaton: {filename}")
    plt.tight_layout()
    plt.savefig(f'Images/{filename}.png')
    plt.show()
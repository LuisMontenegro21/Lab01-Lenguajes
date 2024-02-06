
#----------------------------------------
# Clases del AFD
#----------------------------------------

# Archivo para la conversión del AFN a un AFD mediante construcción de subconjuntos
from graphviz import Digraph


class DFA:
    def __init__(self, num_states, states, num_alphabet, alphabet, start, num_final, final_states, num_transitions, transitions):
        self.num_states = num_states
        self.states = states
        self.num_alphabet = num_alphabet
        self.alphabet = alphabet
        self.start = start
        self.num_final = num_final
        self.final_states = final_states
        self.num_transitions = num_transitions
        self.transitions = transitions

        self.graph = Digraph()
        self.alphabet.append('ε')
        self.num_alphabet = num_alphabet + 1

        # para llenar los estados en states_dict
        self.states_dict = dict()
        for i in range(self.num_states):
            self.states_dict[self.states[i]] = i

        # para llenar los caracteres del alfabeto en alphabet_dict
        self.alphabet_dict = dict()
        for i in range(self.num_alphabet):
            self.alphabet_dict[self.alphabet[i]] = i
        

        # para crear la tabla de transiciones (vacía)
        self.transition_table = dict()
        for transition in transitions:
            current_state, symbol, next_state = transition
            key = (current_state, symbol)  # Use a tuple (current_state, symbol) as the key
            next_state_index = states.index(next_state)  # Find the index of the next state
            self.transition_table[key] = next_state_index

        
        for i in range(self.num_transitions):
            current_state = self.transitions[i][0]
            input_symbol = self.transitions[i][1]
            next_state = self.transitions[i][2]

            # chequear si la transición es None (epsilon) y manejarla acorde
            if input_symbol is None:
                self.transition_table[str(self.states_dict[current_state]) + str(self.alphabet_dict['ε'])].append(self.states_dict[next_state])
            else:
                self.transition_table[str(self.states_dict[current_state]) + str(self.alphabet_dict[input_symbol])].append(self.states_dict[next_state])
    
    def epsilon_closure(self, state):
        # DSF para la epsilon closure
        epsilon_closure_set = set()

        # Stack para el DFS
        stack = [state]

        while stack:
            current_state = stack.pop()

            # Incluir el estado actual 
            epsilon_closure_set.add(current_state)

            # Chequear las transiciones epsilon para el estado actual
            epsilon_symbol_index = str(self.alphabet_dict['ε'])
            epsilon_transitions = self.transition_table.get(str(current_state) + epsilon_symbol_index, [])



            # Añadir el estado si no está aún en el set
            for next_state in epsilon_transitions:
                if next_state not in epsilon_closure_set:
                    stack.append(next_state)

        return epsilon_closure_set
    
    def create_new_state(self, state_set):
        """
        Create a new state in the DFA for the given set of NFA states.
        """
        # Assign a unique name or identifier to the new state
        new_state = "q" + str(len(self.states))
        
        # Add the new state to the set of states
        self.states.append(new_state)
        
        # Update the state dictionary
        self.states_dict[new_state] = len(self.states) - 1
        
        # Return the name of the new state
        return new_state

    def compute_transition(self, state_set, input_symbol):
        """
        Compute the next state set for a given input symbol and state set.
        """
        next_state_set = set()

        for state in state_set:
            transitions = self.transition_table.get(str(self.states_dict[state]) + str(self.alphabet_dict[input_symbol]), [])
            next_state_set.update(transitions)

        # Take epsilon closures for each state in the computed set
        result_set = set()
        for state in next_state_set:
            result_set.update(self.epsilon_closure(state))

        return result_set
    
    def subset_construction(self):
        """
        Apply the subset construction algorithm to convert NFA to DFA.
        """
        # Initialize the DFA with the epsilon closure of the start state
        initial_state_set = self.epsilon_closure(self.start)
        initial_dfa_state = self.create_new_state(initial_state_set)

        # Initialize the queue for processing new states
        state_queue = [(initial_dfa_state, initial_state_set)]

        while state_queue:
            current_dfa_state, current_state_set = state_queue.pop(0)

            for input_symbol in self.alphabet:
                if input_symbol == 'ε':
                    continue

                next_state_set = self.compute_transition(current_state_set, input_symbol)

                if not next_state_set:
                    continue

                if next_state_set not in state_queue:
                    # Create a new state in the DFA for the computed set of NFA states
                    new_dfa_state = self.create_new_state(next_state_set)
                    state_queue.append((new_dfa_state, next_state_set))

                # Add a transition from the current DFA state to the new DFA state
                self.transition_table[str(self.states_dict[current_dfa_state]) + str(self.alphabet_dict[input_symbol])] = self.states_dict[new_dfa_state]


    def generate_dot_file(self, filename='dfa_graph'):
        """
        Generate a DOT file representing the DFA.
        """
        dot = Digraph()

        # Add states
        for state in self.states:
            dot.node(state, shape='circle')
            if state in self.final_states:
                dot.node(state, shape='doublecircle')

        # Add transitions
        for state in self.states:
            for symbol in self.alphabet:
                if symbol == 'ε':
                    continue
                next_state_index = self.transition_table.get(str(self.states_dict[state]) + str(self.alphabet_dict[symbol]), None)
                print(next_state_index)
                if next_state_index is not None:
                    next_state = next_state_index  # Use next_state_index to get the name of the next state
                    dot.edge(state, next_state, label=symbol)


        # Save DOT file
        dot.render(filename, format='png', cleanup=True)   



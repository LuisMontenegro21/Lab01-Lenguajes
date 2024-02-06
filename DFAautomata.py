
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
        for i in range(self.num_states):
            for j in range(self.num_alphabet):
                self.transition_table[str(i)+str(j)] = []

        
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
            epsilon_transitions = self.transition_table.get(str(self.states_dict[current_state]) + str(self.alphabet_dict['ε']), [])

            # Añadir el estado si no está aún en el set
            for next_state in epsilon_transitions:
                if next_state not in epsilon_closure_set:
                    stack.append(next_state)

        return epsilon_closure_set
    
       
        


        






    def graphing(self, nfa):
        #graficando el AFD
        nfa.graph = Digraph()
        for i in nfa.getStates():
            if (i not in [nfa.stateS.number, nfa.stateE.number]):
                nfa.graph.attr('node', shape='circle')
                nfa.graph.node(str(i))
            elif i == nfa.stateE.number:
                nfa.graph.attr('node', shape='doublecircle')
                nfa.graph.node(str(i))
            else:
                nfa.graph.attr('node', shape='circle')
                nfa.graph.node(str(i))
        nfa.graph.attr('node', shape = 'none')
        nfa.graph.node('')
        nfa.graph.edge('', str(nfa.stateS.number))   

        for i in nfa.getTransitions():
            nfa.graph.edge(i[0], i[2], label = ('ε', i[1])[i[1] != 'ε'])
        nfa.graph.render('nfa', view = True)

        #graficando el AFD
        dfa = Digraph()
        epsilon_closure = dict()
        for i in nfa.stateS.states:
            epsilon_closure[i] = list(self.epsilonClosure(i))
        
        dfa_stack = list()
        dfa_stack.append(epsilon_closure[nfa.stateS.number])

        if (nfa.isFinalStateDFA(dfa_stack[0])):
            dfa.attr('node', shape = 'doublecircle')
        else:
            dfa.attr('node', shape = 'circle')
        dfa.node(nfa.stateName(dfa_stack[0]))

        dfa.attr('node', shape = 'none')
        dfa.node('')
        dfa.edge('', nfa.stateName(dfa_stack[0]))

        dfa_states = list()
        dfa_states.append(epsilon_closure[nfa.start])

        while(len(dfa_stack) > 0):
            curr_state = dfa_stack.pop(0)
            for all in range (nfa.num_alphabet - 1):
                from_closure = set()
                for i in curr_state:
                    from_closure.update(set(nfa.transition_table[str(i)+str(all)]))
                if (len(from_closure) > 0):
                    to_state = set()
                    for i in list(from_closure):
                        to_state.update(set(epsilon_closure[nfa.states[i]]))
                    if list(to_state) not in dfa_states:
                        dfa_stack.append(list(to_state))
                        dfa_states.append(list(to_state))

                        if (nfa.isFinalStateDFA(list(to_state))):
                            dfa.attr('node', shape = 'doublecircle')
                        else:
                            dfa.attr('node', shape = 'circle')
                        dfa.node(nfa.stateName(list(to_state)))
                    
                    dfa.edge((nfa.stateName(curr_state)), nfa.stateName(list(to_state)), label=nfa.alphabet[all])

                else:
                    if (-1) not in dfa_states:
                        dfa.attr('node', shape = 'circle')
                        dfa.node('e')

                        for a in range (nfa.num_alphabet - 1):
                            dfa.edge('e', 'e', nfa.alphabet[a])
                        
                        dfa_states.append(-1)

                    dfa.edge(nfa.stateName(curr_state), 'e', label = nfa.alphabet[all])
        dfa.render('dfa', view = True)     

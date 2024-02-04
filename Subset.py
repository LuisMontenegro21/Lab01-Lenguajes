# Archivo para la conversión del AFN a un AFD mediante construcción de subconjuntos
from graphviz import Digraph

class AFD:
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
        self.alphabet.append('e' or 'ε')
        self.num_alphabet = num_alphabet + 1

        self.states_dict = dict()
        for i in range(self.num_states):
            self.states_dict[self.states[i]] = i
        self.alphabet_dict = dict()
        for i in range(self.num_alphabet):
            self.alphabet_dict[self.alphabet[i]] = i

        self.transition_table = dict()
        for i in range(self.num_states):
            for j in range(self.num_alphabet):
                self.transition_table[str(i)+str(j)] = []
        for i in range(self.num_transitions):
            self.transition_table[str(self.states_dict[self.transitions[i][0]]) + str(self.alphabet_dict[self.transitions[i][1]])].append(self.states_dict[self.transitions[i][2]])
        
    
    
    def epsilonClosure(self, state):
        #Se crea un diccionario para ver si el estado ya ha sido visitado
        #y un array va a 
        closure = dict()
        closure[self.states_dict[state]] = 0
        closure_stack = [self.states_dict[state]]
        
        while(len(closure_stack) > 0):
            curr = closure_stack.pop(0)
            for i in self.transition_table[str(curr)+str(self.alphabet_dict['e' or 'ε'])]:
                if i not in closure.keys():
                    closure[i] = 0
                    closure_stack.append(i)
            closure[curr] = 1
        return closure.keys()
    
    # ver el nombre del estado en que se está
    def stateName(self, state_list):
        name = ''
        for i in state_list:
            name += self.states[i]
        return name
    
    # ver si el estado en el que está es estado final
    def isFinalStateDFA(self, state_list):
        for i in state_list:
            for j in self.final_states:
                if (i == self.states_dict[j]):
                    return True
        return False

    def graphing(self, nfa):
        #graficando el AFD
        nfa.graph = Digraph()
        for i in nfa.states:
            if (i not in nfa.final_states):
                nfa.graph.attr('node', shape = 'circle')
                nfa.graph.node(i)
            else: 
                nfa.graph.attr('node', shape = 'doublecircle')
                nfa.graph.node(i)
        nfa.graph.attr('node', shape = 'none')
        nfa.graph.node('')
        nfa.graph.edge('', nfa.start)   

        for i in nfa.transitions:
            nfa.graph.edge(i[0], i[2], label = ('ε', i[1])[i[1] != 'e'])
        nfa.graph.render('nfa', view = True)

        #graficando el AFD
        dfa = Digraph()
        epsilon_closure = dict()
        for i in nfa.states:
            epsilon_closure[i] = list(nfa.epsilonClosure(i))
        
        dfa_stack = list()
        dfa_stack.append(epsilon_closure[nfa.start])

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
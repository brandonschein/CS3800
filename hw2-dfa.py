class DFA:
    def __init__(self, states, alphabet, transitions, start, accepts):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions 
        self.start = start
        self.accepts = accepts

def get_transition(cur_state, symbol, transition_list):
    for i in transition_list:
        if(i[0] == cur_state and i[1] == symbol):
            return i[2]
    else:
        return "No Transition Found"

def run(dfa, str_input): 
    current_state = dfa.start
    input_split = list(str_input)

    for cur_symbol in input_split:
        current_state = get_transition(current_state, cur_symbol, dfa.transitions)
    
    accepted = False

    for i in dfa.accepts: 
        if(i == current_state):
            accepted = True

    if(accepted):
        print("accept")
    else:
        print("reject")

#get the input 
try:
    input_string = input()
except EOFError:
    print("Invalid input")

#sets up the elements used to create a DFA
states = ["q1", "q2", "q3"]
alphabet = ["0", "1"]
delta = [["q1", "0", "q1"], ["q1", "1", "q2"], ["q2", "0", "q3"], ["q2", "1", "q2"], ["q3", "0", "q2"], ["q3", "1", "q2"]]
start_state = "q1"
accept_states = ["q2"]

#creates the DFA to use as an example in testing 
testDFA = DFA(states, alphabet, delta, start_state, accept_states)

run(testDFA, input_string)


# how DFA's will be represented in my 
class DFA:
    def __init__(self, states, alphabet, transitions, start, accepts):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions 
        self.start = start
        self.accpets = accepts

#get the input 
try:
    to_ret = input()
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

# determing what to do based off of the input given 
if(to_ret == "states"):
    for i in testDFA.states:
        print(i)
elif(to_ret == "alpha"):
    for i in testDFA.alphabet:
        print(i)
elif(to_ret == "transitions"):
    for x in testDFA.transitions:
        print(" ".join(x))
elif(to_ret == "start"):
    print(testDFA.start)
elif(to_ret == "accepts"):
    for i in testDFA.accpets:
        print(i)
        
else:
    print("Invalid Input")

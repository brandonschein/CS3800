DFA Data Representation: 

A state is represented by a string
A symbol is a 1-char string

A DFA is (states, alpha, transitions, start, accepts):
- states is a list of the states in the automaton
- alpha is the accepted alphabet of the automaton
- transitions is a 2 dimensional array, which contains a list of lists where the lists describe the transitions as a list of size 3 with the 1st element being the starting state of the transition, the 2nd element being the symbol from the alphabet that the transition acts on, and the 3rd element being the state that is being transitioned to. 
- start is a string that tells the name of the start stae (i.e. "q1")
- accepts is a list of states that the automaton accepts

Time Spent: 1:30 hour

Resources: 
 - lecture slides/notes

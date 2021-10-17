DFA Data Representation: 

-A state is represented by a string
-A symbol is a 1-char string

A DFA is (states, alpha, transitions, start, accepts):
- states is a list of the states in the automaton, where each state is a string denoting the name of the state
- alpha is the accepted alphabet of the automaton, where each symbol in the alphabet is a single character string
- transitions is a 2 dimensional array (an array of arrays), which contains a list of lists where the lists describe the transitions as a list of size 3 with the 1st element being the starting state of the transition, the 2nd element being the symbol from the alphabet that the transition acts on, and the 3rd element being the state that is being transitioned to. 
- start is a string that tells the name of the start stae (i.e. "q1")
- accepts is a list of states that the automaton accepts, the list of states are in the form where each state is denoted by a string representing the name of the state


NFA Data Representation:

-A state is represented by a string 
-A symbol is a 1-char string

An NFA is (states, alpha, transitions, start, accepts):

- states is a list of the states in the automaton, where each state is a string denoting the name of the state
- alpha is the accepted alphabet of the automaton, where each symbol in the alphabet is a single character string 
- transitions is a 2 dimensional array(an array of arrays), which contains a list of lists where the lists describe the transitions as a list of size 3 with the 1st element being the starting state of the transition, the 2nd element being the symbol from the alphabet that the transition acts on, and the 3rd element being the state that is being transitioned to. In an NFA, a symbol can be None, representing an epsilon in which no input is read in order to traverse the transition list. 
- start is a string that tells the name of the start state (i.e. "q1") 
- accepts is a list of states that the automaton accepts, the list of states are in the form where each state is denoted by a string representing the name of the state


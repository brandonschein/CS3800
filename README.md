PDA Data Representation: 

A state is represented by a string
A symbol is a 1-char string

An NFA is (states, inp_alpha, stack_alpha, transitions, start, accepts):

-states is a list of the states in the automaton
-inp_alpha is the input alphabet of the automaton
-stack_alpha is the stack alphabet of the automaton
-transitions is a dictionary, which contains the elements of each transition
1st element being the starting state of the transition, the 2nd element being the symbol from the alphabet that the transition acts on, and the 3rd element being the state that is being transitioned to.
-start is a string that tells the name of the start state (i.e. "q1")
accepts is a list of states that the automaton accepts
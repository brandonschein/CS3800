CFG Data Representation: 

A state is represented by a string A symbol is a 1-char string

A CFG is (variables, terminals, rules, start):

Where:
variables is a set holding the designated variables of the CFG, characters which have productions
terminals is a list holding all of the designated terminals of the CFG, characters which do not have any productions
rules is a dictionary that holds the productions of the CFG. Productions are modeled in such a way that the left side holds the variable and the right side holds all possible productions of that variable. the rules variable itself holds all of these productions in its dictionary.
start is the starting variable character of the CFG

Time taken: 10 hours

Resources used: 
- Slides
- lecture notes

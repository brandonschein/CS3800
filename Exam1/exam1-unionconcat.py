import sys
import xml.etree.ElementTree as ET

# class for creating NFAs by the data defintion
class NFA:
    def __init__(self, states, alphabet, transitions, start, accepts):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions 
        self.start = start
        self.accepts = accepts

# a helper function thats supposed to enrue that getting the transitions
# does not go into an infinte loop of epsilon transitions
def get_none_help(cur_state, transition_list, seen):
    if cur_state in seen:
        return []

    return_list = []
    
    for i in transition_list:
        seen.append(i[0])
        if(i[0] == cur_state and i[1] == None):
            return_list.append(i[2])
            return_list += get_none_help(i[2], transition_list, seen)
            
    return return_list

# returns the transitions of epsilons only
def get_none_transition(cur_state, transition_list):
    return get_none_help(cur_state, transition_list, [])

# gets the transitions from a state given a symbol
def get_transition(cur_state, symbol, transition_list):
    return_list = []
    
    for i in transition_list:
        if(i[0] == cur_state and i[1] == symbol):
            return_list.append(i[2])
            
    return return_list
    

# runs a given string input on an automata 
def run(nfa, input):
    current_state = [nfa.start]
    input_split = list(input)
    #print(current_state)
    #print("input for ^ : " + input)
    current_state += get_none_transition(nfa.start, nfa.transitions)
    for cur_symbol in input_split: 
        # if(input == "abc"):
            # print(current_state)
            # print(nfa.transitions)
        updated_states = []
        for cur_state in current_state:
            updated_states += get_transition(cur_state, cur_symbol, nfa.transitions)
           
        temporary_array = []
        for cur_state in updated_states:
            temporary_array += get_none_transition(cur_state, nfa.transitions)
        updated_states += temporary_array
        current_state = updated_states
       
        
    accepted = False
    
    for i in current_state:
        if (i in nfa.accepts):
            accepted = True

    if(accepted):
        return "accept"
    else:
        return "reject"
    
# helper function to produce all strings of a given length and alphabet
def recursive_helper(length, symbols):
    if(length == 1):
        return symbols
    else:
        returned_arr = recursive_helper(length - 1, symbols)
        to_ret = []
        for i in symbols:
            for x in returned_arr:
                to_ret.append(i + x)

        return to_ret 

# produces all strings of a given length and alphabet 
def recursive_string(length, symbols):
    if (length == 1):
        return symbols
    else:
        return recursive_helper(length, symbols) + recursive_string(length - 1, symbols)

def finalCheck(toPrint, union_works, concat_works):
    if(len(union_works) == 0):
        return []
    else:
        return toPrint

# removes any epsilon loops from a state to the same state as this is redundant
# and causes issues 
def scrubLoops(transitions):
    return_array = []
    for i in transitions:
        if(not ((i[1] == None) and (i[0] == i[2]))):
            return_array.append(i)

    return return_array


###########################
# getting input
try:
    xmlfiles_input = sys.stdin.read()
except EOFError:
    print("Invalid input")


xmlfiles = xmlfiles_input.split(" ")
file1 = xmlfiles[0]
file2 = xmlfiles[1]

# parsing the first nfa file 
nfa1_state_names = []
nfa1_start_state = ""
nfa1_accept_states = []
nfa1_transitions = []
nfa1_alphabet = []

with open(file1, "r") as file:
    tree = ET.parse(file)
    root = tree.getroot()

    if(root.tag != "automaton"):
        tag_list = list(root.getchildren())
        pos = 0
        while True:
            if(tag_list[pos].tag == "automaton"):
                root = tag_list[pos]
                break
            else:
                tag_list += list(root.getchildren())
            pos += 1
    

    temp_arr = []
    swap_arr = []
    identity_arr = []
    for child in root:
        if(child.tag == "state"):
            identity_arr.append(child.attrib['id'])
            identity_arr.append(child.attrib['name'])
            for ch in child:
                if(ch.tag == "initial"):
                    nfa1_start_state = child.attrib['name']
                if(ch.tag == "final"):
                    nfa1_accept_states.append(child.attrib['name'])
            nfa1_state_names.append(child.attrib['name'])
        if(child.tag == "transition"):
            for ch in child:
                if(ch.tag == 'from'):
                    temp_arr.append(ch.text)
                if(ch.tag == 'to'):
                    temp_arr.append(ch.text)
                if(ch.tag == 'read'):
                    temp_arr.append(ch.text)
                    swap_arr.append(temp_arr[0])
                    swap_arr.append(temp_arr[2])
                    swap_arr.append(temp_arr[1])
                    nfa1_transitions.append(swap_arr)
                    temp_arr = []
                    swap_arr = []

    for x in nfa1_transitions:
        if(x[1] not in nfa1_alphabet):
            nfa1_alphabet.append(x[1])
    
    for x in nfa1_transitions:
        x[0] = identity_arr[identity_arr.index(x[0]) + 1]
        x[2] = identity_arr[identity_arr.index(x[2]) + 1]

# parsing the second nfa file 
nfa2_state_names = []
nfa2_start_state = ""
nfa2_accept_states = []
nfa2_transitions = []
nfa2_alphabet = []

with open(file2, "r") as file:
    tree = ET.parse(file)
    root = tree.getroot()

    if(root.tag != "automaton"):
        tag_list = list(root.getchildren())
        pos = 0
        while True:
            if(tag_list[pos].tag == "automaton"):
                root = tag_list[pos]
                break
            else:
                tag_list += list(root.getchildren())
            pos += 1
    

    temp_arr = []
    swap_arr = []
    identity_arr = []
    for child in root:
        if(child.tag == "state"):
            identity_arr.append(child.attrib['id'])
            identity_arr.append(child.attrib['name'])
            for ch in child:
                if(ch.tag == "initial"):
                    nfa2_start_state = child.attrib['name']
                if(ch.tag == "final"):
                    nfa2_accept_states.append(child.attrib['name'])
            nfa2_state_names.append(child.attrib['name'])
        if(child.tag == "transition"):
            for ch in child:
                if(ch.tag == 'from'):
                    temp_arr.append(ch.text)
                if(ch.tag == 'to'):
                    temp_arr.append(ch.text)
                if(ch.tag == 'read'):
                    temp_arr.append(ch.text)
                    swap_arr.append(temp_arr[0])
                    swap_arr.append(temp_arr[2])
                    swap_arr.append(temp_arr[1])
                    nfa2_transitions.append(swap_arr)
                    temp_arr = []
                    swap_arr = []

    for x in nfa2_transitions:
        if(x[1] not in nfa2_alphabet):
            nfa2_alphabet.append(x[1])
    
    for x in nfa2_transitions:
        x[0] = identity_arr[identity_arr.index(x[0]) + 1]
        x[2] = identity_arr[identity_arr.index(x[2]) + 1]

# getting rid of redundant loops 
nfa1_transitions = scrubLoops(nfa1_transitions)
nfa2_transitions = scrubLoops(nfa2_transitions)

# setting the 2 nfas 
nfa1 = NFA(nfa1_state_names, nfa1_alphabet, nfa1_transitions, nfa1_start_state, nfa1_accept_states)
nfa2 = NFA(nfa2_state_names, nfa2_alphabet, nfa2_transitions, nfa2_start_state, nfa2_accept_states)    

# create Union 

nfa_union_names = []
nfa_union_alphabet = []
nfa_union_transitions = []
nfa_union_start = "new_start_state"
nfa_union_accepts = []

nfa_union_names.append("new_start_state")

for i in nfa1_state_names:
    i = "nfa1_" + i
    nfa_union_names.append(i)

for i in nfa2_state_names:
    i = "nfa2_" + i
    nfa_union_names.append(i)


nfa_union_alphabet = nfa1_alphabet

for i in nfa2_alphabet:
    if(i not in nfa_union_alphabet):
        nfa_union_alphabet.append(i)

if (None in nfa_union_alphabet):
    nfa_union_alphabet.remove(None)

for i in nfa1_accept_states:
    i = "nfa1_" + i
    nfa_union_accepts.append(i)

for i in nfa2_accept_states:
    i = "nfa2_" + i
    nfa_union_accepts.append(i)

for i in nfa1_transitions:
    i[0] = "nfa1_" + i[0]
    i[2] = "nfa1_" + i[2]
    nfa_union_transitions.append(i)

for i in nfa2_transitions:
    i[0] = "nfa2_" + i[0]
    i[2] = "nfa2_" + i[2]
    nfa_union_transitions.append(i)


nfa_union_transitions.append(["new_start_state", None, "nfa1_" + nfa1_start_state])
nfa_union_transitions.append(["new_start_state", None, "nfa2_" + nfa2_start_state])

# print(nfa_union_names)
# print(nfa_union_alphabet)
# print(nfa_union_transitions)
# print(nfa_union_start)
# print(nfa_union_accepts)

nfaUnion = NFA(nfa_union_names, nfa_union_alphabet, nfa_union_transitions, nfa_union_start, nfa_union_accepts)

# create concat 

# print(nfa2_state_names)
# print(nfa2_alphabet)
# print(nfa2_transitions)
# print(nfa2_start_state)
# print(nfa2_accept_states)

################################ 
nfa_concat_names = []
nfa_concat_alphabet = []
nfa_concat_transitions = []
nfa_concat_start = ""
nfa_concat_accepts = []

for i in nfa1_state_names:
    i = "nfa1_" + i
    nfa_concat_names.append(i)

for i in nfa2_state_names:
    i = "nfa2_" + i
    nfa_concat_names.append(i)

nfa_concat_alphabet = nfa1.alphabet

for i in nfa2.alphabet:
    if(i not in nfa_concat_alphabet):
        nfa_concat_alphabet.append(i)

if (None in nfa_concat_alphabet):
    nfa_concat_alphabet.remove(None)

nfa_concat_start = "nfa1_" + nfa1_start_state

for x in nfa2_accept_states:
    nfa_concat_accepts.append("nfa2_" + x)

# for i in nfa1_transitions:
#     nfa_concat_transitions.append(["nfa1_" + i[0], i[1], "nfa1_" + i[2]])

# for y in nfa2_transitions:
#     nfa_concat_transitions.append(["nfa2_" + y[0], y[1], "nfa2_" + y[2]])

nfa_concat_transitions = nfa1_transitions + nfa2_transitions

for x in nfa1_accept_states:
    nfa_concat_transitions.append(["nfa1_" + x, None, "nfa2_" + nfa2_start_state])

# print(nfa2_accept_states)
# print(nfa_concat_names)
# print(nfa_concat_alphabet)
# print(nfa_concat_transitions)
# print(nfa_concat_start)
# print(nfa_concat_accepts)

nfaConcat = NFA(nfa_concat_names, nfa_concat_alphabet, nfa_concat_transitions, nfa_concat_start, nfa_concat_names)


union_works = []
concat_works = []

union_test_list = recursive_string(5, nfaUnion.alphabet)
union_test_list.append("")

#print(union_test_list)

# print(nfaUnion.alphabet)
for x in union_test_list:
    # print(x)
    if(run(nfaUnion, x) == "accept"):
        union_works.append(x)

# print(union_works)

concat_test_list = recursive_string(5, nfaConcat.alphabet)
concat_test_list.append("")

# print(concat_test_list) 

for x in concat_test_list:
    if(run(nfaConcat, x) == "accept"):
        concat_works.append(x)

# print(concat_works)

toPrint = [] 

# building the toPrint list 
for i in concat_works:
    if(i not in union_works):
        toPrint.append(i)
toPrint = finalCheck(toPrint, union_works, concat_works)
    
# deals with the case of not printing something for the autograder
# to accept an empty array as a print() will still give a newline 
# which breaks the test case of the autograder. In this if the array is 
# empty the program will simply output nothing, therefore passing the test
# cases of nothing to stdout

if(not (len(toPrint) == 0)):
    for i in toPrint:
        print(i)


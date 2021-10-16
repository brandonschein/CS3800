import xml.etree.cElementTree as ET
import sys
from itertools import combinations

stringToTest = sys.stdin.read()

bddF1 = "bddF1.xml"
bddF2 = "bddF2.xml"
bddF3 = "bddF3.xml"

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
        return "accept"
    else:
        return "reject"


file1_state_names = []
file1_start_state = ""
file1_accept_states = []
file1_transitions = []
file1_alphabet = []



with open(bddF1, "r") as file:
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
                    file1_start_state = child.attrib['name']
                if(ch.tag == "final"):
                    file1_accept_states.append(child.attrib['name'])
            file1_state_names.append(child.attrib['name'])
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
                    file1_transitions.append(swap_arr)
                    temp_arr = []
                    swap_arr = []

    for x in file1_transitions:
        if(x[1] not in file1_alphabet):
            file1_alphabet.append(x[1])
    
    for x in file1_transitions:
        x[0] = identity_arr[identity_arr.index(x[0]) + 1]
        x[2] = identity_arr[identity_arr.index(x[2]) + 1]


cur_file = bddF2

file2_state_names = []
file2_start_state = ""
file2_accept_states = []
file2_transitions = []
file2_alphabet = []

with open(cur_file, "r") as file:
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
                    file2_start_state = child.attrib['name']
                if(ch.tag == "final"):
                    file2_accept_states.append(child.attrib['name'])
            file2_state_names.append(child.attrib['name'])
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
                    file2_transitions.append(swap_arr)
                    temp_arr = []
                    swap_arr = []

    for x in file2_transitions:
        if(x[1] not in file2_alphabet):
            file2_alphabet.append(x[1])
    
    for x in file2_transitions:
        x[0] = identity_arr[identity_arr.index(x[0]) + 1]
        x[2] = identity_arr[identity_arr.index(x[2]) + 1]


cur_file = bddF3

file3_state_names = []
file3_start_state = ""
file3_accept_states = []
file3_transitions = []
file3_alphabet = []

with open(cur_file, "r") as file:
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
                    file3_start_state = child.attrib['name']
                if(ch.tag == "final"):
                    file3_accept_states.append(child.attrib['name'])
            file3_state_names.append(child.attrib['name'])
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
                    file3_transitions.append(swap_arr)
                    temp_arr = []
                    swap_arr = []

    for x in file3_transitions:
        if(x[1] not in file3_alphabet):
            file3_alphabet.append(x[1])
    
    for x in file3_transitions:
        x[0] = identity_arr[identity_arr.index(x[0]) + 1]
        x[2] = identity_arr[identity_arr.index(x[2]) + 1]


# print(stringToTest)
# print(file1_state_names)
# print(file1_alphabet)
# print(file1_transitions)
# print(file1_start_state)
# print(file1_accept_states)

# print(file2_state_names)
# print(file2_alphabet)
# print(file2_transitions)
# print(file2_start_state)
# print(file2_accept_states)

# print(file3_state_names)
# print(file3_alphabet)
# print(file3_transitions)
# print(file3_start_state)
# print(file3_accept_states)



dfa1 = DFA(file1_state_names, file1_alphabet, file1_transitions, file1_start_state, file1_accept_states)
dfa2 = DFA(file2_state_names, file2_alphabet, file2_transitions, file2_start_state, file2_accept_states)

unionDFA_states = []
unionDFA_alphabet = []
unionDFA_transitions = []
unionDFA_start = ""
unionDFA_accept = []


for x in dfa1.states:
    for y in dfa2.states:
        unionDFA_states.append(x + " " + y)
        



unionDFA_alphabet = dfa1.alphabet
for i in dfa2.alphabet:
    if(i not in unionDFA_alphabet):
        unionDFA_alphabet.append(i)



unionDFA_start = dfa1.start + " " + dfa2.start


for x in dfa1.accepts:
    for y in dfa2.states:
        unionDFA_accept.append(x + " " + y)
        
for x in dfa1.states:
    for y in dfa2.accepts: 
        unionDFA_accept.append(x+ " " + y)
        
    


# get transition list 
for i in unionDFA_states:
    a, b = i.split(" ")
    for alp in unionDFA_alphabet:
        dfa1_to = get_transition(a, alp, dfa1.transitions)
        dfa2_to = get_transition(b, alp, dfa2.transitions)
        unionDFA_transitions.append([i, alp, dfa1_to + " " + dfa2_to])


# print(unionDFA_states)
# print(unionDFA_alphabet)
# print(unionDFA_transitions)
# print(unionDFA_start)
# print(unionDFA_accept)

newDFA = DFA(unionDFA_states, unionDFA_alphabet, unionDFA_transitions, unionDFA_start, unionDFA_accept)
dfa3 = DFA(file3_state_names, file3_alphabet, file3_transitions, file3_start_state, file3_accept_states)

bddDFA_states = []
bddDFA_alphabet = []
bddDFA_transitions = []
bddDFA_start = ""
bddDFA_accept = []


for x in newDFA.states:
    for y in dfa3.states:
        bddDFA_states.append(x + " " + y)
        



bddDFA_alphabet = newDFA.alphabet

for i in dfa3.alphabet:
    if(i not in bddDFA_alphabet):
        bddDFA_alphabet.append(i)



bddDFA_start = newDFA.start + " " + dfa3.start


for x in newDFA.accepts:
    for y in dfa3.states:
        bddDFA_accept.append(x + " " + y)
        
for x in newDFA.states:
    for y in dfa3.accepts: 
        bddDFA_accept.append(x+ " " + y)
        
    


# get transition list 
for i in bddDFA_states:
    a, b, c = i.split(" ")
    for alp in bddDFA_alphabet:
        newDFA_to = get_transition(a + " " + b, alp, newDFA.transitions)
        dfa3_to = get_transition(c, alp, dfa3.transitions)
        bddDFA_transitions.append([i, alp, newDFA_to + " " + dfa3_to])

bddDFA = DFA(bddDFA_states, bddDFA_alphabet, bddDFA_transitions, bddDFA_start, bddDFA_accept)


print(run(bddDFA, stringToTest))




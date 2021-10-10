import sys
import xml.etree.cElementTree as ET

class NFA:
    def __init__(self, states, alphabet, transitions, start, accepts):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions 
        self.start = start
        self.accepts = accepts

# def get_transitions(cur_states, cur_symbol, transitions_list):
#     return_list = []
    
#     for x in cur_states:
#         temp_arr = []
#         for y in transitions_list:
#             if((y[0] == x and y[1] == cur_symbol) or (y[0] == x and y[1] == None)):
#                 temp_arr.append(y[2])
#         if(len(temp_arr) == 0):
#             cur_states.remove(x)
#         else:
#             return_list += temp_arr
    
#     return return_list

def get_none_transition(cur_state, transition_list):
    return_list = []
    
    for i in transition_list:
        if(i[0] == cur_state and i[1] == None):
            return_list.append(i[2])
            
    return return_list

def get_transition(cur_state, symbol, transition_list):
    return_list = []
    
    for i in transition_list:
        if(i[0] == cur_state and i[1] == symbol):
            return_list.append(i[2])
            
    return return_list
    


def run(nfa, input):
    current_state = [nfa.start]
    input_split = list(input)
    current_state += get_none_transition(nfa.start, nfa.transitions)
    for cur_symbol in input_split: 
        updated_states = []
        for cur_state in current_state:
            updated_states += get_transition(cur_state, cur_symbol, nfa.transitions)
        for cur_state in updated_states:
            updated_states += get_none_transition(cur_state, nfa.transitions)
        current_state = updated_states
        
        
    
    accepted = False
    
    for i in current_state:
        if (i in nfa.accepts):
            accepted = True

    if(accepted):
        return "accept"
    else:
        return "reject"

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


def recursive_string(length, symbols):
    if (length == 1):
        return symbols
    else:
        return recursive_helper(length, symbols) + recursive_string(length - 1, symbols)

try:
    xmlfile = sys.stdin.read()
except EOFError:
    print("Invalid input")

nfa_state_names = []
nfa_start_state = ""
nfa_accept_states = []
nfa_transitions = []
nfa_alphabet = []

with open(xmlfile, "r") as file:
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
                    nfa_start_state = child.attrib['name']
                if(ch.tag == "final"):
                    nfa_accept_states.append(child.attrib['name'])
            nfa_state_names.append(child.attrib['name'])
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
                    nfa_transitions.append(swap_arr)
                    temp_arr = []
                    swap_arr = []

    for x in nfa_transitions:
        if(x[1] not in nfa_alphabet):
            nfa_alphabet.append(x[1])
    
    for x in nfa_transitions:
        x[0] = identity_arr[identity_arr.index(x[0]) + 1]
        x[2] = identity_arr[identity_arr.index(x[2]) + 1]



# print(nfa_state_names)
# print(nfa_alphabet)
# print(nfa_transitions)
# print(nfa_start_state)
# print(nfa_accept_states)
if(None in nfa_alphabet):
    nfa_alphabet.remove(None)

xmlNFA = NFA(nfa_state_names, nfa_alphabet, nfa_transitions, nfa_start_state, nfa_accept_states)

works = []

test_list = recursive_string(5, xmlNFA.alphabet)
test_list.append("")


for x in test_list:
    if(run(xmlNFA, x) == "accept"):
        works.append(x)


for y in works:
    print("".join(y))
    




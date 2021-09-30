import xml.etree.cElementTree as ET
from itertools import combinations

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

xmlfile = input()

state_names = []
start_state = ""
accept_states = []
transitions = []
alphabet = []

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
                tag_list + list(root.getchildren())
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
                    start_state = child.attrib['name']
                if(ch.tag == "final"):
                    accept_states.append(child.attrib['name'])
            state_names.append(child.attrib['name'])
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
                    transitions.append(swap_arr)
                    temp_arr = []
                    swap_arr = []

    for x in transitions:
        if(x[1] not in alphabet):
            alphabet.append(x[1])
    
    for x in transitions:
        x[0] = identity_arr[identity_arr.index(x[0]) + 1]
        x[2] = identity_arr[identity_arr.index(x[2]) + 1]

    xmlDFA = DFA(state_names, alphabet, transitions, start_state, accept_states)
    
    works = []

    for x in recursive_string(5, xmlDFA.alphabet):
        if(run(xmlDFA, x) == "accept"):
            works.append(x)
    
    for y in works:
        print("".join(y))
        
        
  



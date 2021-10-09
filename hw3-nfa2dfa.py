import sys
from typing import NewType 
import xml.etree.cElementTree as ET

class DFA:
    def __init__(self, states, alphabet, transitions, start, accepts):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions 
        self.start = start
        self.accepts = accepts



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

nfa_alphabet.remove(None)

# print(nfa_state_names)
# print(nfa_alphabet)
# print(nfa_transitions)
# print(nfa_start_state)
# print(nfa_accept_states)

dfa_state_names = []
dfa_start_state = ""
dfa_accept_states = []
dfa_transitions = []
dfa_alphabet = []

dfa_alphabet = nfa_alphabet

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

def get_none_transition(cur_state, transition_list):
    return get_none_help(cur_state, transition_list, [])

def get_transition(cur_state, symbol, transition_list):
    return_list = []
    
    for i in transition_list:
        if(i[0] == cur_state and i[1] == symbol):
            return_list.append(i[2])
            
    return return_list

from itertools import combinations

temp_start_state = set([nfa_start_state] + get_none_transition(nfa_start_state, nfa_transitions))

for i in range (1, len(nfa_state_names) + 1):
    for element in combinations(nfa_state_names, i):
        element = list(element)
        element.sort()
        state_str = " ".join(element)
        if set(element) == temp_start_state:
            dfa_start_state = state_str

        for n in nfa_accept_states:
            if(n in element):
                dfa_accept_states.append(state_str)

        for x in nfa_alphabet:
            temp_arr = []
            for y in element:
                temp_arr += get_transition(y, x, nfa_transitions)
                temp_arr += get_none_transition(y, nfa_transitions)
            new_temp = []
            for z in temp_arr:
                new_temp += get_none_transition(z, nfa_transitions)
            temp_arr += new_temp
            temp_arr = list(set(temp_arr))
            temp_arr.sort()
            
            if len(temp_arr) > 0:
                dfa_transitions.append([state_str, x, " ".join(temp_arr)])


        dfa_state_names.append(state_str)

newDFA = DFA(dfa_state_names, dfa_alphabet, dfa_transitions, dfa_start_state, dfa_accept_states)

root = ET.Element("automaton")

swap_arr = []
for i in range(0, len(newDFA.states)):
    cur_state = ET.SubElement(root, "state", id=str(i), name=newDFA.states[i])
    swap_arr.append(str(i))
    swap_arr.append(newDFA.states[i])

    if(newDFA.states[i] == newDFA.start):
        ET.SubElement(cur_state, "initial")
    if(newDFA.states[i] in newDFA.accepts):
        ET.SubElement(cur_state, "final")

for i in newDFA.transitions:
    cur_transition = ET.SubElement(root, "transition")
    ET.SubElement(cur_transition, "from").text = swap_arr[swap_arr.index(i[0]) - 1]
    ET.SubElement(cur_transition, "to").text = swap_arr[swap_arr.index(i[2]) - 1]
    ET.SubElement(cur_transition, "read").text = i[1]

tree = ET.ElementTree(root)
tree.write(sys.stdout, encoding="unicode")

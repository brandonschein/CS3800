import xml.etree.cElementTree as ET
import sys
from itertools import combinations

xmlfiles = sys.stdin.read().split(" ")

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

cur_file = xmlfiles[0]

file1_state_names = []
file1_start_state = ""
file1_accept_states = []
file1_transitions = []
file1_alphabet = []



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


cur_file = xmlfiles[1]

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




newDFA = DFA(unionDFA_states, unionDFA_alphabet, unionDFA_transitions, unionDFA_start, unionDFA_accept)

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



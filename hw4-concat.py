import sys
import xml.etree.ElementTree as ET

class NFA:
    def __init__(self, states, alphabet, transitions, start, accepts):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions 
        self.start = start
        self.accepts = accepts


try:
    xmlfiles_input = sys.stdin.read()
except EOFError:
    print("Invalid input")

xmlfiles = xmlfiles_input.split(" ")
file1 = xmlfiles[0]
file2 = xmlfiles[1]

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


nfa1 = NFA(nfa1_state_names, nfa1_alphabet, nfa1_transitions, nfa1_start_state, nfa1_accept_states)

nfa2 = NFA(nfa2_state_names, nfa2_alphabet, nfa2_transitions, nfa2_start_state, nfa2_accept_states)    


nfa_union_names = []
nfa_union_alphabet = []
nfa_union_transitions = []
nfa_union_start = ""
nfa_union_accepts = []

for i in nfa1_state_names:
    i = "nfa1_" + i
    nfa_union_names.append(i)

for i in nfa2_state_names:
    i = "nfa2_" + i
    nfa_union_names.append(i)

nfa_union_alphabet = nfa1.alphabet

for i in nfa2.alphabet:
    if(i not in nfa_union_alphabet):
        nfa_union_alphabet.append(i)

nfa_union_start = nfa1_start_state

nfa_union_accepts = nfa2_accept_states


for x in nfa1_transitions:
    if(x[2] in nfa1_accept_states):
        nfa1_transitions.append([x[2], None, nfa2_start_state])

nfa_union_transitions = nfa1_transitions
nfa_union_transitions += nfa2_transitions

# print(nfa_union_names)
# print(nfa_union_alphabet)
# print(nfa_union_transitions)
# print(nfa_union_start)
# print(nfa_union_accepts)

nfaUnion = NFA(nfa_union_names, nfa_union_alphabet, nfa_union_transitions, nfa_union_start, nfa_union_accepts)

root = ET.Element("automaton")

swap_arr = []

for i in range(0, len(nfaUnion.states)):
    cur_state = ET.SubElement(root, "state", id=str(i), name=nfaUnion.states[i])
    swap_arr.append(str(i))
    swap_arr.append(nfaUnion.states[i])

    if(nfaUnion.states[i] == nfaUnion.start):
        ET.SubElement(cur_state, "initial")
    if(nfaUnion.states[i] in nfaUnion.accepts):
        ET.SubElement(cur_state, "final")

# print(swap_arr)
for i in nfaUnion.transitions:
    cur_transition = ET.SubElement(root, "transition")
    ET.SubElement(cur_transition, "from").text = swap_arr[swap_arr.index(i[0]) - 1]
    ET.SubElement(cur_transition, "to").text = swap_arr[swap_arr.index(i[2]) - 1]
    ET.SubElement(cur_transition, "read").text = i[1]

tree = ET.ElementTree(root)
tree.write(sys.stdout, encoding="unicode")

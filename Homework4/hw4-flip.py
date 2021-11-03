import sys
import xml.etree.ElementTree as ET

class NFA:
    def __init__(self, states, alphabet, transitions, start, accepts):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions 
        self.start = start
        self.accepts = accepts

def print_nfa(nfa):
    root = ET.Element("automaton")

    swap_arr = []

    for i in range(0, len(nfa.states)):
        cur_state = ET.SubElement(root, "state", id=str(i), name=nfa.states[i])
        swap_arr.append(str(i))
        swap_arr.append(nfa.states[i])

        if(nfa.states[i] == nfa.start):
            ET.SubElement(cur_state, "initial")
        if(nfa.states[i] in nfa.accepts):
            ET.SubElement(cur_state, "final")

    # print(swap_arr)
    for i in nfa.transitions:
        cur_transition = ET.SubElement(root, "transition")
        ET.SubElement(cur_transition, "from").text = swap_arr[swap_arr.index(i[0]) - 1]
        ET.SubElement(cur_transition, "to").text = swap_arr[swap_arr.index(i[2]) - 1]
        ET.SubElement(cur_transition, "read").text = i[1]

    tree = ET.ElementTree(root)
    tree.write(sys.stdout, encoding="unicode")


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

nss = "new_start_state"
nfa_flip_states = []
nfa_flip_alphabet = []
nfa_flip_transitions = []
nfa_flip_start = nss
nfa_flip_accepts = []

nfa_flip_states = nfa_state_names
nfa_flip_states.append(nss)

nfa_flip_alphabet = nfa_alphabet

for i in nfa_transitions:
    nfa_flip_transitions.append([i[2], i[1], i[0]])

nfa_flip_accepts.append(nfa_start_state)

for i in nfa_accept_states:
    nfa_flip_transitions.append([nss, None, i])


nfaFlip = NFA(nfa_flip_states, nfa_flip_alphabet, nfa_flip_transitions, nfa_flip_start, nfa_flip_accepts)

print_nfa(nfaFlip)

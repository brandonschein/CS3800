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
nfa_kleene_names = [nss]
nfa_kleene_alphabet = nfa_alphabet
nfa_kleene_transitions = []
nfa_kleene_start = nss
nfa_kleene_accepts = [nss]

nfa_kleene_names += nfa_state_names


nfa_kleene_accepts += nfa_accept_states

nfa_kleene_transitions = nfa_transitions

nfa_kleene_transitions.append([nss, None, nfa_start_state])

for x in nfa_accept_states:
    nfa_kleene_transitions.append([x, None, nfa_start_state])


# print(nfa_kleene_names)
# print(nfa_kleene_alphabet)
# print(nfa_kleene_transitions)
# print(nfa_kleene_start)
# print(nfa_kleene_accepts)

nfaKleene = NFA(nfa_kleene_names, nfa_kleene_alphabet, nfa_kleene_transitions, nfa_kleene_start, nfa_kleene_accepts)
root = ET.Element("automaton")

swap_arr = []

for i in range(0, len(nfaKleene.states)):
    cur_state = ET.SubElement(root, "state", id=str(i), name=nfaKleene.states[i])
    swap_arr.append(str(i))
    swap_arr.append(nfaKleene.states[i])

    if(nfaKleene.states[i] == nfaKleene.start):
        ET.SubElement(cur_state, "initial")
    if(nfaKleene.states[i] in nfaKleene.accepts):
        ET.SubElement(cur_state, "final")

# print(swap_arr)
for i in nfaKleene.transitions:
    cur_transition = ET.SubElement(root, "transition")
    ET.SubElement(cur_transition, "from").text = swap_arr[swap_arr.index(i[0]) - 1]
    ET.SubElement(cur_transition, "to").text = swap_arr[swap_arr.index(i[2]) - 1]
    ET.SubElement(cur_transition, "read").text = i[1]

tree = ET.ElementTree(root)
tree.write(sys.stdout, encoding="unicode")
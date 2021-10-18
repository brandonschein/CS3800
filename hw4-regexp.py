import sys
import xml.etree.ElementTree as ET

class NFA:
    def __init__(self, states, alphabet, transitions, start, accepts):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions 
        self.start = start
        self.accepts = accepts


runNum = input()

def make_single_char_nfa(c):
    c = str(c)
    nfa_states = ["q0", "q1", "q2"]
    nfa_alphabet = [c]
    nfa_transitions = [["q0", c, "q1"], ["q1", c, "q2"], ["q2", c, "q2"]]
    nfa_start = "q0"
    nfa_accept = ["q1"]

    return NFA(nfa_states, nfa_alphabet, nfa_transitions, nfa_start, nfa_accept)

def make_single_char_kleene(c):
    c = str(c)
    nfa_states = ["q0"]
    nfa_alphabet = [c]
    nfa_transitions = [["q0", c, "q0"]]
    nfa_start = "q0"
    nfa_accept = ["q0"]

    return NFA(nfa_states, nfa_alphabet, nfa_transitions, nfa_start, nfa_accept)

def make_kleene(nfa):
    nss = "new_start_state" + nfa.start

    kleene_states = nfa.states
    kleene_alphabet = nfa.alphabet
    kleene_transitions = nfa.transitions
    kleene_start = nss
    kleene_accept = nfa.accepts

    kleene_states.append(nss)
    kleene_accept.append(nss)

    kleene_transitions.append([nss, None, nfa.start])

    for i in nfa.accepts:
        kleene_transitions.append([i, None, nfa.start])

    return NFA(kleene_states, kleene_alphabet, kleene_transitions, kleene_start, kleene_accept)

def make_concat(nfa1, nfa2):
    concat_states = []
    concat_alphabet = []
    concat_transitions = []
    concat_start = "nfa1_" + nfa1.start
    concat_accept = []

    for i in nfa1.states:
        concat_states.append("nfa1_" + i)
    for i in nfa2.states:
        concat_states.append("nfa2_" + i)

    concat_alphabet = nfa1.alphabet
    for i in nfa2.alphabet:
        if(i not in concat_alphabet):
            concat_alphabet.append(i)

    for i in nfa1.transitions:
        concat_transitions.append(["nfa1_" + i[0], i[1], "nfa1_" + i[2]])
    for i in nfa2.transitions:
        concat_transitions.append(["nfa2_" + i[0], i[1], "nfa2_" + i[2]])
    for i in nfa1.accepts:
        concat_transitions.append(["nfa1_" + i, None, "nfa2_" + nfa2.start])

    for i in nfa2.accepts:
        concat_accept.append("nfa2_" + i)

    return NFA(concat_states, concat_alphabet, concat_transitions, concat_start, concat_accept)
    
def make_union(nfa1, nfa2):
    nss = "new_start_state" + nfa1.start
    union_states = []
    union_alphabet = []
    union_transitions = []
    union_start = nss
    union_accepts = []

    for i in nfa1.states:
        union_states.append("nfa1_" + i)
    for i in nfa2.states:
        union_states.append("nfa2_" + i)
    union_states.append(nss)
    
    union_alphabet = nfa1.alphabet
    for i in nfa2.alphabet:
        if(i not in union_alphabet):
            union_alphabet.append(i)

    for i in nfa1.transitions:
        union_transitions.append(["nfa1_" + i[0], i[1], "nfa1_" + i[2]])
    for i in nfa2.transitions:
        union_transitions.append(["nfa2_" + i[0], i[1], "nfa2_" + i[2]])
    union_transitions.append([nss, None, "nfa1_" + nfa1.start])
    union_transitions.append([nss, None, "nfa2_" + nfa2.start])

    

    for i in nfa1.accepts:
        union_accepts.append("nfa1_" + i)
    for i in nfa2.accepts:
        union_accepts.append("nfa2_" + i)

    return NFA(union_states, union_alphabet, union_transitions, union_start, union_accepts)
    
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

runNum = int(runNum)

if (runNum == 1):
   print_nfa(make_concat(make_concat(make_single_char_kleene(0), make_single_char_nfa(1)), make_single_char_kleene(0)))
elif (runNum == 2):
    print_nfa(make_concat(make_concat(make_concat(make_concat(make_kleene(make_union(make_single_char_nfa(0), make_single_char_nfa(1))), make_single_char_nfa(0)), make_single_char_nfa(0)), make_single_char_nfa(1)), make_kleene(make_union(make_single_char_nfa(0), make_single_char_nfa(1)))))
elif (runNum == 3):
    print_nfa(make_concat(make_single_char_kleene(1), make_kleene(make_concat(make_single_char_nfa(0), make_concat(make_single_char_nfa(1), make_single_char_kleene(1))))))
# elif (runNum == 4):
#     # TODO
# elif (runNum == 5):
#     # TODO
# elif (runNum == 6):
#     # TODO
# elif (runNum == 7):
#     # TODO
# elif (runNum == 8):
#     # TODO
# else:
#    print("invalid")

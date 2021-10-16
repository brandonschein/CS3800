import sys
import xml.etree.ElementTree as ET

class NFA:
    def __init__(self, states, alphabet, transitions, start, accepts):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions 
        self.start = start
        self.accepts = accepts


# making the nfa for the task 

nfa_lang_states = ["q0", "q1", "q2", "q3", "q4", "q5", "q6"]
nfa_lang_alphabet = ["0", "1", "2"]
nfa_lang_transitions = [["q0", "0", "q1"], ["q0", "1", "q1"], ["q0", "2", "q1"], 
["q1", "0", "q2"], ["q1", "1", "q2"], ["q1", "2", "q2"],
["q2", "0", "q3"], ["q2", "1", "q6"], ["q2", "2", "q6"],
["q3", "0", "q4"], ["q3", "1", "q4"], ["q3", "2", "q4"],
["q4", "0", "q5"], ["q4", "1", "q5"], ["q4", "2", "q5"],
["q5", "0", "q3"], ["q5", "1", "q6"], ["q5", "2", "q6"],
["q6", "0", "q6"], ["q6", "1", "q6"], ["q6", "2", "q6"]]
nfa_lang_start = "q0"
nfa_lang_accepts = ["q0", "q1", "q2", "q3"]

nfaLang = NFA(nfa_lang_states, nfa_lang_alphabet, nfa_lang_transitions, nfa_lang_start, nfa_lang_accepts)

root = ET.Element("automaton")

swap_arr = []

for i in range(0, len(nfaLang.states)):
    cur_state = ET.SubElement(root, "state", id=str(i), name=nfaLang.states[i])
    swap_arr.append(str(i))
    swap_arr.append(nfaLang.states[i])

    if(nfaLang.states[i] == nfaLang.start):
        ET.SubElement(cur_state, "initial")
    if(nfaLang.states[i] in nfaLang.accepts):
        ET.SubElement(cur_state, "final")

# print(swap_arr)
for i in nfaLang.transitions:
    cur_transition = ET.SubElement(root, "transition")
    ET.SubElement(cur_transition, "from").text = swap_arr[swap_arr.index(i[0]) - 1]
    ET.SubElement(cur_transition, "to").text = swap_arr[swap_arr.index(i[2]) - 1]
    ET.SubElement(cur_transition, "read").text = i[1]

tree = ET.ElementTree(root)
tree.write(sys.stdout, encoding="unicode")
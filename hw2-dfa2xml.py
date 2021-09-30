import xml.etree.cElementTree as ET

class DFA:
    def __init__(self, states, alphabet, transitions, start, accepts):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions 
        self.start = start
        self.accepts = accepts

DFA_states = ["q0", "q1", "q2", "q3", "q4"]
DFA_alphabet = ["0", "1"]
DFA_transitions = [["q0", "0", "q0"], ["q0", "1", "q1"], ["q1", "0", "q1"], ["q1", "1", "q2"], 
["q2", "0", "q2"], ["q2", "1", "q3"], ["q3", "0", "q3"], ["q3", "1", "q4"], ["q4", "0", "q4"], ["q4", "1", "q4"]]
DFA_start = "q0"
DFA_accepts = ["q3"]

xmlDFA = DFA(DFA_states, DFA_alphabet, DFA_transitions, DFA_start, DFA_accepts)


automaton = ET.Element("automaton")

swap_arr = []
for i in range(0, len(xmlDFA.states)):
    cur_state = ET.SubElement(automaton, "state", id=str(i), name=xmlDFA.states[i])
    swap_arr.append(str(i))
    swap_arr.append(xmlDFA.states[i])

    if(xmlDFA.states[i] == xmlDFA.start):
        ET.SubElement(cur_state, "initial")
    if(xmlDFA.states[i] in xmlDFA.accepts):
        ET.SubElement(cur_state, "final")

for i in xmlDFA.transitions:
    cur_transition = ET.SubElement(automaton, "transition")
    ET.SubElement(cur_transition, "from").text = swap_arr[swap_arr.index(i[0]) - 1]
    ET.SubElement(cur_transition, "to").text = swap_arr[swap_arr.index(i[2]) - 1]
    ET.SubElement(cur_transition, "read").text = i[1]

tree = ET.ElementTree(automaton)
tree.write("threeDFA.xml")

import sys
import xml.etree.cElementTree as ET

class PDA:
    def __init__(self, states, alphabet, stack_alphabet, transitions, start, accepts):
        self.states = states
        self.alphabet = alphabet
        self.stack_alphabet = stack_alphabet
        self.transitions = transitions
        self.start = start
        self.accepts = accepts

def PDAtoXML(pda):
    root = ET.Element("structure")
    ET.SubElement(root, "type").text = "pda"
    automaton = ET.SubElement(root, "automaton")
    for state in range(0, len(pda.states) - 1):
        cur_state = ET.SubElement(automaton, "state", id=str(state), name=pda.states[state])
        if pda.states[state] == pda.start:
            ET.SubElement(cur_state, "initial")
        if pda.states[state] in pda.accepts:
            ET.SubElement(cur_state, "final")

    for key in pda.transitions:
        right_side = pda.transitions[key]
        transition = ET.SubElement(automaton, "transition")
        for list in right_side:
            ET.SubElement(transition, "from").text = str(key[0])
            ET.SubElement(transition, "to").text = str(key[1])
            ET.SubElement(transition, "read").text = str(list[0])
            ET.SubElement(transition, "pop").text = str(list[1])
            ET.SubElement(transition, "push").text = str(list[2])
    
    tree = ET.ElementTree(root)
    tree.write(sys.stdout, encoding="unicode") 

pdaw_states = ['q0', 'q1', 'q2', 'q3']
pdaw_alphabet = ['[', ']', '(', ')']
pdaw_stack_alphabet = ['SS', ']', 'E', '(', '[', 'CD', 'D', 'F', 'AF', 'B', 'AB', 'A', ')', 'SD', '$', 'S', 'CE', 'C', 'SB']
# structure (from, to): (read, pop, push)
pdaw_transitions = {('q0', 'q3'): [('', '', '$')],
                    ('q1', 'q1'): [('[', '[', ''), ('(', '(', ''), (']', ']', ''),
                                    (')', ')', ''), ('', 'S', 'AB'), ('', 'S', 'CD'),
                                    ('', 'S', 'SS'), ('', 'S', ''), ('', 'E', 'SD'),
                                    ('', 'S', 'AF'), ('', 'C', '('), ('', 'D', ')'),
                                    ('', 'A', '['), ('', 'B', ']')],
                    ('q1', 'q2'): [('', '$', '')],
                    ('q3', 'q1'): [('', '', '$')]}
pdaw_start = 'q0'
pdaw_accepts = 'q2'

pdaw = PDA(pdaw_states, pdaw_alphabet, pdaw_stack_alphabet, pdaw_transitions, pdaw_start, pdaw_accepts)

PDAtoXML(pdaw)

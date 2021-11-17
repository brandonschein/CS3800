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
        print(state)
        cur_state = ET.SubElement(automaton, "state", id=str(state), name="q" + str(state))
        if pda.states[state] == pda.start:
            ET.SubElement(cur_state, "initial")
        if pda.states[state] in pda.accepts:
            ET.SubElement(cur_state, "final")

    for key in pda.transitions:
        right_side = pda.transitions[key]
        print(right_side)
        transition = ET.SubElement(automaton, "transition")
        for list in right_side:
            ET.SubElement(transition, "from").text = str(key)
            ET.SubElement(transition, "to").text = str(list[0])
            ET.SubElement(transition, "read").text = str(list[1])
            ET.SubElement(transition, "push").text = str(list[2])
            ET.SubElement(transition, "pop").text = str(list[3])
    
    tree = ET.ElementTree(root)
    tree.write(sys.stdout, encoding="unicode") 

pdaw_states = ['q0', 'q1', 'q2']
pdaw_alphabet = ['[', ']', '(', ')']
pdaw_stack_alphabet = ['[', ']', '(', ')']
pdaw_transitions = {0: [[1, None, '$', None]], 1: [[1, '[', '[', None], [1, '(', '(', None], [1, ']', None, ']'], [1, ')', None, ')'], [2, None, None, "$"]]}
pdaw_start = 'q0'
pdaw_accepts = 'q2'

pdaw = PDA(pdaw_states, pdaw_alphabet, pdaw_stack_alphabet, pdaw_transitions, pdaw_start, pdaw_accepts)

PDAtoXML(pdaw)

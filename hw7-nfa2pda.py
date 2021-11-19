import sys
import xml.etree.cElementTree as ET
from itertools import combinations

class NFA:
    def __init__(self, states, alphabet, transitions, start, accepts):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions 
        self.start = start
        self.accepts = accepts

class PDA:
    def __init__(self, states, alphabet, stack_alphabet, transitions, start, accepts):
        self.states = states
        self.alphabet = alphabet
        self.stack_alphabet = stack_alphabet
        self.transitions = transitions
        self.start = start
        self.accepts = accepts

def parseNFA(file):
    nfa_state_names = []
    nfa_start_state = ""
    nfa_accept_states = []
    nfa_transitions = []
    nfa_alphabet = []
    with open(file, "r"):
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
    if(None in nfa_alphabet):
        nfa_alphabet.remove(None)

    return NFA(nfa_state_names, nfa_alphabet, nfa_transitions, nfa_start_state, nfa_accept_states)

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


def nfa2pda(nfa):
    pda_states = []
    pda_alphabet = []
    pda_stack_alphabet = [] 
    pda_transitions = {} #build
    pda_start = ""
    pda_accepts = []

    pda_states = nfa.states
    pda_start = nfa.start
    pda_accepts = nfa.accepts
    pda_alphabet = nfa.alphabet

    for transition in nfa.transitions:
        #print(transition)
        pda_transitions[(transition[0], transition[2])] = [(transition[1], '', '')]

    # idea, go through all of dfa's states and transitions and write them into PDA's and have the read pop and pull be NONE, 
    # basically not doing a pda 

    #another idea, just do thi swith an nfa too ? 
    return PDA(pda_states, pda_alphabet, pda_stack_alphabet, pda_transitions, pda_start, pda_accepts)
##########################################################
input_file = input()
parsedNFA = parseNFA(input_file)
newPDA = nfa2pda(parsedNFA)
#print(newPDA.transitions)
PDAtoXML(newPDA)


# print(parsedNFA.states)
# print(parsedNFA.alphabet)
# print(parsedNFA.transitions)
# print(parsedNFA.start)
# print(parsedNFA.accpets)

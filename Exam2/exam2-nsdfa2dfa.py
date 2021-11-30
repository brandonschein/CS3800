import sys
import xml.etree.cElementTree as ET

class nsDFA():
    def __init__(self, states, alphabet, transitions, start, accepts) :
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.starts = start
        self.accepts = accepts

class DFA:
    def __init__(self, states, alphabet, transitions, start, accepts):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions 
        self.start = start
        self.accepts = accepts
def DFAtoXML(dfa):
    root = ET.Element("automaton")

    swap_arr = []
    for i in range(0, len(dfa.states)):
        cur_state = ET.SubElement(root, "state", id=str(i), name=dfa.states[i])
        swap_arr.append(str(i))
        swap_arr.append(dfa.states[i])

        if(dfa.states[i] == dfa.start):
            ET.SubElement(cur_state, "initial")
        if(dfa.states[i] in dfa.accepts):
            ET.SubElement(cur_state, "final")

    for i in dfa.transitions:
        cur_transition = ET.SubElement(root, "transition")
        ET.SubElement(cur_transition, "from").text = swap_arr[swap_arr.index(i[0]) - 1]
        ET.SubElement(cur_transition, "to").text = swap_arr[swap_arr.index(i[2]) - 1]
        ET.SubElement(cur_transition, "read").text = i[1]

    tree = ET.ElementTree(root)
    tree.write(sys.stdout, encoding="unicode")


def parsensDFA(xmlfile):
    state_names = []
    start_state = []
    accept_states = []
    transitions = []
    alphabet = []

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
                        start_state.append(child.attrib['name'])
                    if(ch.tag == "final"):
                        accept_states.append(child.attrib['name'])
                state_names.append(child.attrib['name'])
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
                        transitions.append(swap_arr)
                        temp_arr = []
                        swap_arr = []

        for x in transitions:
            if(x[1] not in alphabet):
                alphabet.append(x[1])
        
        for x in transitions:
            x[0] = identity_arr[identity_arr.index(x[0]) + 1]
            x[2] = identity_arr[identity_arr.index(x[2]) + 1]

        return nsDFA(state_names, alphabet, transitions, start_state, accept_states)

def get_transition(cur_state, symbol, transition_list):
    for i in transition_list:
        if(i[0] == cur_state and i[1] == symbol):
            return i[2]
    else:
        return "No Transition Found"

def unionDFA(dfa1, dfa2):
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




    return DFA(unionDFA_states, unionDFA_alphabet, unionDFA_transitions, unionDFA_start, unionDFA_accept)

def nsDFAtoDFA(nsDFA):
    DFAtoUnion = []
    for start in nsDFA.starts:
        temp_dfa = DFA(nsDFA.states, nsDFA.alphabet, nsDFA.transitions, start, nsDFA.accepts)
        DFAtoUnion.append(temp_dfa)
    
    while(len(DFAtoUnion) > 1):
        temp_dfa = unionDFA(DFAtoUnion[0], DFAtoUnion[1])
        DFAtoUnion.pop(0)
        DFAtoUnion.pop(0)
        DFAtoUnion.append(temp_dfa)

    return DFAtoUnion[0]
    




###########################################

file = sys.stdin.read()
exam_nsDFA = parsensDFA(file)

# print(exam_nsDFA.states)
# print(exam_nsDFA.alphabet)
# print(exam_nsDFA.transitions)
# print(exam_nsDFA.start)
# print(exam_nsDFA.accepts)

exam_dfa = nsDFAtoDFA(exam_nsDFA)
DFAtoXML(exam_dfa)

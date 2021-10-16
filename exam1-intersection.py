import sys 
import xml.etree.cElementTree as ET

class DFA:
    def __init__(self, states, alphabet, transitions, start, accepts):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions 
        self.start = start
        self.accepts = accepts

def get_transition(cur_state, symbol, transition_list):
    for i in transition_list:
        if(i[0] == cur_state and i[1] == symbol):
            return i[2]
    else:
        return "No Transition Found"


def run(dfa, str_input): 
    current_state = dfa.start
    input_split = list(str_input)

    for cur_symbol in input_split:
        current_state = get_transition(current_state, cur_symbol, dfa.transitions)
    
    accepted = False

    for i in dfa.accepts: 
        if(i == current_state):
            accepted = True

    if(accepted):
        return "valid"
    else:
        return "invalid"

def intersect(dfa1, dfa2):
    file1_state_names = []
    file1_start_state = ""
    file1_accept_states = []
    file1_transitions = []
    file1_alphabet = []

    with open(dfa1, "r") as file:
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
                        file1_start_state = child.attrib['name']
                    if(ch.tag == "final"):
                        file1_accept_states.append(child.attrib['name'])
                file1_state_names.append(child.attrib['name'])
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
                        file1_transitions.append(swap_arr)
                        temp_arr = []
                        swap_arr = []

        for x in file1_transitions:
            if(x[1] not in file1_alphabet):
                file1_alphabet.append(x[1])
        
        for x in file1_transitions:
            x[0] = identity_arr[identity_arr.index(x[0]) + 1]
            x[2] = identity_arr[identity_arr.index(x[2]) + 1]


   

    file2_state_names = []
    file2_start_state = ""
    file2_accept_states = []
    file2_transitions = []
    file2_alphabet = []

    with open(dfa2, "r") as file:
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
                        file2_start_state = child.attrib['name']
                    if(ch.tag == "final"):
                        file2_accept_states.append(child.attrib['name'])
                file2_state_names.append(child.attrib['name'])
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
                        file2_transitions.append(swap_arr)
                        temp_arr = []
                        swap_arr = []

        for x in file2_transitions:
            if(x[1] not in file2_alphabet):
                file2_alphabet.append(x[1])
        
        for x in file2_transitions:
            x[0] = identity_arr[identity_arr.index(x[0]) + 1]
            x[2] = identity_arr[identity_arr.index(x[2]) + 1]


    dfa1 = DFA(file1_state_names, file1_alphabet, file1_transitions, file1_start_state, file1_accept_states)
    dfa2 = DFA(file2_state_names, file2_alphabet, file2_transitions, file2_start_state, file2_accept_states)

    intersectDFA_states = []
    intersectDFA_alphabet = []
    intersectDFA_transitions = []
    intersectDFA_start = ""
    intersectDFA_accept = []


    for x in dfa1.states:
        for y in dfa2.states:
            intersectDFA_states.append(x + " " + y)
            



    intersectDFA_alphabet = dfa1.alphabet
    for i in dfa2.alphabet:
        if(i not in intersectDFA_alphabet):
            intersectDFA_alphabet.append(i)



    intersectDFA_start = dfa1.start + " " + dfa2.start




    for x in dfa1.accepts:
        for y in dfa2.accepts:
            intersectDFA_accept.append(x + " " + y)
            

    # get transition list 
    for i in intersectDFA_states:
        a, b = i.split(" ")
        for alp in intersectDFA_alphabet:
            dfa1_to = get_transition(a, alp, dfa1.transitions)
            dfa2_to = get_transition(b, alp, dfa2.transitions)
            intersectDFA_transitions.append([i, alp, dfa1_to + " " + dfa2_to])


    # print(intersectDFA_states)
    # print(intersectDFA_alphabet)
    # print(intersectDFA_transitions)
    # print(intersectDFA_start)
    # print(intersectDFA_accept)

    intersectDFA = DFA(intersectDFA_states, intersectDFA_alphabet, intersectDFA_transitions, intersectDFA_start, intersectDFA_accept)

    return intersectDFA

# "main" starts here 
stringToTest = sys.stdin.read()

A1 = "IntersectA1.xml"
A2 = "IntersectA2.xml"
A3 = "IntersectA3.xml"
A4 = "IntersectA4.xml"

intersect1 = intersect(A1, A2)

# root = ET.Element("automaton")

# swap_arr = []

# for i in range(0, len(intersect1.states)):
#     cur_state = ET.SubElement(root, "state", id=str(i), name=intersect1.states[i])
#     swap_arr.append(str(i))
#     swap_arr.append(intersect1.states[i])

#     if(intersect1.states[i] == intersect1.start):
#         ET.SubElement(cur_state, "initial")
#     if(intersect1.states[i] in intersect1.accepts):
#         ET.SubElement(cur_state, "final")

# # print(swap_arr)
# for i in intersect1.transitions:
#     cur_transition = ET.SubElement(root, "transition")
#     ET.SubElement(cur_transition, "from").text = swap_arr[swap_arr.index(i[0]) - 1]
#     ET.SubElement(cur_transition, "to").text = swap_arr[swap_arr.index(i[2]) - 1]
#     ET.SubElement(cur_transition, "read").text = i[1]

# tree = ET.ElementTree(root)
# tree.write("A1A2intersect.xml")

intersect2 = intersect(A3, A4)

# root = ET.Element("automaton")

# swap_arr = []

# for i in range(0, len(intersect2.states)):
#     cur_state = ET.SubElement(root, "state", id=str(i), name=intersect2.states[i])
#     swap_arr.append(str(i))
#     swap_arr.append(intersect2.states[i])

#     if(intersect2.states[i] == intersect2.start):
#         ET.SubElement(cur_state, "initial")
#     if(intersect2.states[i] in intersect2.accepts):
#         ET.SubElement(cur_state, "final")

# # print(swap_arr)
# for i in intersect2.transitions:
#     cur_transition = ET.SubElement(root, "transition")
#     ET.SubElement(cur_transition, "from").text = swap_arr[swap_arr.index(i[0]) - 1]
#     ET.SubElement(cur_transition, "to").text = swap_arr[swap_arr.index(i[2]) - 1]
#     ET.SubElement(cur_transition, "read").text = i[1]

# tree = ET.ElementTree(root)
# tree.write("A3A4intersect.xml")
# finalIntersect = intersect(intersect2, A4)



final_intersectDFA_states = []
final_intersectDFA_alphabet = []
final_intersectDFA_transitions = []
final_intersectDFA_start = ""
final_intersectDFA_accept = []


for x in intersect1.states:
    for y in intersect2.states:
        final_intersectDFA_states.append(x + " " + y)
        



final_intersectDFA_alphabet = intersect1.alphabet
for i in intersect2.alphabet:
    if(i not in final_intersectDFA_alphabet):
        final_intersectDFA_alphabet.append(i)



final_intersectDFA_start = intersect1.start + " " + intersect2.start




for x in intersect1.accepts:
    for y in intersect2.accepts:
        final_intersectDFA_accept.append(x + " " + y)
        

# get transition list 
for i in final_intersectDFA_states:
    a, b, c, d = i.split(" ")
    for alp in final_intersectDFA_alphabet:
        dfa1_to = get_transition(a + " " + b, alp, intersect1.transitions)
        dfa2_to = get_transition(c + " " + d, alp, intersect2.transitions)
        final_intersectDFA_transitions.append([i, alp, dfa1_to + " " + dfa2_to])


finalIntersectDFA = DFA(final_intersectDFA_states, final_intersectDFA_alphabet, final_intersectDFA_transitions, final_intersectDFA_start, final_intersectDFA_accept)


print(run(finalIntersectDFA, stringToTest))
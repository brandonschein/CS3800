import sys
from collections import defaultdict
import xml.etree.cElementTree as ET

class PDA:
    def __init__(self, states, alphabet, stack_alphabet, transitions, start, accepts):
        self.states = states
        self.alphabet = alphabet
        self.stack_alphabet = stack_alphabet
        self.transitions = transitions
        self.start = start
        self.accepts = accepts


def parse(filename):
        data = ET.parse(filename)
        root = data.getroot()

        # Find automaton names
        id_name_dict = dict()
        start = ""
        accepts = []
        # finds the state elements whether or not automaton is the root of the Element Tree
        for child in root.findall("./automaton/state") + root.findall("./state"):
            id_name_dict[child.attrib['id']] = child.attrib['name']
            initial = child.find("initial")
            if initial is not None:
                start = child.attrib['name']
            final = child.find("final")
            if final is not None:
                accepts.append(child.attrib['name'])
        # prints each segment in the format described in the HW prompt

        # go through delta
        delta = dict()
        alpha = dict()
        tao = set()
        for transition in root.findall("./automaton/transition") + root.findall("./transition"):
            from_state = transition.find('from').text
            to_state = transition.find('to').text
            read = transition.find('read').text
            if read == None:
                read = ""
            else:
                alpha[read] = ""

            pop = transition.find('pop').text
            push = transition.find('push').text

            if pop == None:
                pop = ""
            else:
                tao.add(pop)

            if push == None:
                push = ""
            else:
                tao.add(push)

            state_list = delta.get((id_name_dict[from_state], id_name_dict[to_state]))
            if state_list == None:
                state_list = []
            state_list.append((read, pop, push))
            delta[(id_name_dict[from_state], id_name_dict[to_state])
                  ] = state_list

        return PDA(list(id_name_dict.values()), list(alpha.keys()), tao, delta, start, accepts)

########################################################
input = sys.stdin.read().split(" ")
input_jff = input[0]
run_string = input[1]
run_times = sys.maxsize
if(len(input) == 3):
   run_times = input[3] 

thisPDA = parse(input_jff)

print(thisPDA.states)
print(thisPDA.alphabet)
print(thisPDA.stack_alphabet)
print(thisPDA.transitions)
print(thisPDA.start)
print(thisPDA.accepts)

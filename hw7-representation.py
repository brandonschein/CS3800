#class for PDAs, refer to read me for definition
class PDA:
    def __init__(self, states, inp_alpha, stack_alpha, transitions, start, accepts):
       self.states = variables
       self.inp_alphabet = inp_alphabet
       self.stack_alphabet = stack_alphabet
       self.transitions = transitions
       self.start = start
       self.accept = accept

    
    # takes a CFG and prints it out to stdout
def PDAtoXML(pda):
    root = ET.Element("automaton")

    swap_arr = []
    for i in range(0, len(xmlDFA.states)):
        cur_state = ET.SubElement(root, "state", id=str(i), name=xmlDFA.states[i])
        swap_arr.append(str(i))
        swap_arr.append(xmlDFA.states[i])

        if(xmlDFA.states[i] == xmlDFA.start):
            ET.SubElement(cur_state, "initial")
        if(xmlDFA.states[i] in xmlDFA.accepts):
            ET.SubElement(cur_state, "final")

    for i in xmlDFA.transitions:
        cur_transition = ET.SubElement(root, "transition")
        ET.SubElement(cur_transition, "from").text = swap_arr[swap_arr.index(i[0]) - 1]
        ET.SubElement(cur_transition, "to").text = swap_arr[swap_arr.index(i[2]) - 1]
        ET.SubElement(cur_transition, "read").text = i[1]

    tree = ET.ElementTree(root)
    tree.write(sys.stdout, encoding="unicode")

myPDA = PDA(['a','b'],['l','m'],['x','y'],{},'a',['a','b'])

PDAtoXML(myPDA)
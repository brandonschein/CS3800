import xml.etree.cElementTree as ET

xmlfile = input()

state_names = []
start_state = ""
accept_states = []

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
                tag_list + list(root.getchildren())
            pos += 1
    

    for child in root:

        if(child.tag == "state"):
            for ch in child:
                if(ch.tag == "initial"):
                    start_state = child.attrib['name']
                if(ch.tag == "final"):
                    accept_states.append(child.attrib['name'])
            state_names.append(child.attrib['name'])
    

    
    print(" ".join(state_names))
    print(start_state)
    print(" ".join(accept_states))

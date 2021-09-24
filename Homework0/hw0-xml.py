#importing a library to parse the xml file
import xml.etree.cElementTree as ET

#getting the xmlfile as input
xmlfile = input()

#instaniating up what will be returned
state_names = []
start_state = ""
accept_states = []

#open the file
with open(xmlfile, "r") as file:
    tree = ET.parse(file)
    root = tree.getroot()
    
    #if the initial root tag is not automaton, find it
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
    

    # go through and find all the state tags and add them to the variables
    # according to the task
    for child in root:
        if(child.tag == "state"):
            for ch in child:
                if(ch.tag == "initial"):
                    start_state = child.attrib['name']
                if(ch.tag == "final"):
                    accept_states.append(child.attrib['name'])
            state_names.append(child.attrib['name'])
    

    #print the information
    print(" ".join(state_names))
    print(start_state)
    print(" ".join(accept_states))

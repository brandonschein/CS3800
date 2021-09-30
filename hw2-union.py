import xml.etree.cElementTree as ET

xmlfiles = input()

split_files = xmlfiles.split(" ")

with open(split_files[0], "r") as file1:
    with open(split_files[1], "r") as file2:
        tree1 = ET.parse(file1)
        tree2 = ET.parse(file2)

        root1 = tree1.getroot()
        root2 = tree2.getroot()

        tag_list = []

        if(root1.tag != "automaton"):
            tag_list = list(root1.getchildren())
            pos = 0
            while True:
                if(tag_list[pos].tag == "automaton"):
                    root1 = tag_list[pos]
                    break
                else:
                    tag_list + list(root1.getchildren())
                pos += 1

        tag_list = []

        if(root2.tag != "automaton"):
            tag_list = list(root2.getchildren())
            pos = 0
            while True:
                if(tag_list[pos].tag == "automaton"):
                    root1 = tag_list[pos]
                    break
                else:
                    tag_list + list(root2.getchildren())
                pos += 1

        root1_start_state = ""
        root1_accept_states = []
        root1_state_names = []
        for child in root1:
            if(child.tag == "state"):
                for ch in child:
                    if(ch.tag == "initial"):
                        root1_start_state = child.attrib['name']
                    if(ch.tag == "final"):
                        root1_accept_states.append(child.attrib['name'])
                root1_state_names.append(child.attrib['name'])

        
        root2_start_state = ""
        root2_accept_states = []
        root2_state_names = []
        for child in root2:
            if(child.tag == "state"):
                for ch in child:
                    if(ch.tag == "initial"):
                        root2_start_state = child.attrib['name']
                    if(ch.tag == "final"):
                        root2_accept_states.append(child.attrib['name'])
                root2_state_names.append(child.attrib['name'])

        print(root2_state_names)
        print(root1_state_names)
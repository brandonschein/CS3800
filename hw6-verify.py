import sys
import xml.etree.cElementTree as ET

# get rid of the empty string at the end of the split
verify_arr = sys.stdin.read().split("\n")[:-1]

file = "types.jff"

cfg_variables = []
cfg_terminals = []
cfg_rules = {}
cfg_start = ""

def parseCFG(file):
    with open(file, "r") as file:
        tree = ET.parse(file)
    root = tree.getroot()

    if(root.tag != "structure"):
        tag_list = list(root.getchildren())
        pos = 0
        while True:
            if(tag_list[pos].tag == "structure"):
                root = tag_list[pos]
                break
            else:
                tag_list += list(root.getchildren())
            pos += 1


    for child in root:
        #if(child.tag == "type"):
            # do I need to do anything ? 
            
        if(child.tag == "production"):
            left_text = ""
            for ch in child:
                
                if(ch.tag == "left"):
                    left_text = ch.text
                    if(ch.text not in cfg_rules):
                        cfg_rules[ch.text] = []
                if(ch.tag == "right"):
                    cfg_rules[left_text].append(ch.text)

def verify_helper(str, derv_seq):
    if len(derv_seq) == 0:
        for char in str:
            if char in cfg_variables:
                return False
        return True
    derv = []
    for char in derv_seq[0]:
        derv.append(char)

    variations = [[]]
    for char in str:

        if char in cfg_variables:
            rights = cfg_rules.get(char)

            if rights == None:
                return False

            new_variations = []
            for variation in variations:
                for right in rights:
                    new_variations.append(variation + list(right))
            
            for variation in variations:
                variation.append(char)
            
            variations += new_variations
        else:
            for variation in variations:
                variation.append(char)
    if not (derv in variations):
        return False

    return verify_helper(derv, derv_seq[1:])


def verify(derv_seq):
    start = derv_seq[0]
    rights = cfg_rules.get(start)

    if(rights == None):
        return False
    
    else:
        return verify_helper(start, derv_seq[1:])

#########################################
# main starts here
parseCFG(file)

cfg_start = list(cfg_rules.keys())[0]
     
for i in cfg_rules:
    if(i not in cfg_variables):
        cfg_variables.append(i)

for i in cfg_rules:
    for x in cfg_rules[i]:
        for y in x:
            if(y not in cfg_terminals) and (y not in cfg_variables):
                cfg_terminals.append(y)

# checks to see if the cfg was gotten correctly
# print(cfg_variables)
# print(cfg_terminals)
# print(cfg_rules)
# print(cfg_start)

if(verify(verify_arr)):
    print("accept")
else:
    print("reject")

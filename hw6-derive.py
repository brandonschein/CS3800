import sys
import xml.etree.cElementTree as ET

#class for CFGs, refer to read me for definition
class CFG:
    def __init__(self, variables, terminals, rules, start):
       self.variables = variables
       self.terminals = terminals
       self.rules = rules
       self.start = start

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

def derive(source, target):
    return_arr = []
    for element in derive_helper(source, target, []):
        return_arr.append(''.join(element))
    if(len(return_arr) == 0):
        return None
    else:
        return source + return_arr

def derive_helper(source, target, visited):
    temp_str = ''.join(source)

    if temp_str in visited or len(source) > 1 + len(target):
        return None
    
    visited.append(temp_str)

    for char in source:
        if char not in cfg_variables:
            if ((char not in target) and (char != "")):
                return None

    variations = [[]]

    for char in source:
        if char in cfg_variables:
            prods = cfg_rules[char]

            if prods == None:
                variations = False
            
            new_variations = []
            for variation in variations:
                for right in prods:
                    if (variation != None and right != None):
                        if len(right) == 0:
                            right = []
                        new_variations.append(variation + list(right))
            variations = new_variations
        else:
            for variation in variations:
                variation.append(char)
    

    if target in variations:
        return [target]
    
    for variation in variations:
        ders = derive_helper(variation, target, visited)

        if ders != None:
            return [variation] + ders

    return None


#########################################
# main starts here
file, source, target = sys.stdin.read().split("\n")[:-1]


parseCFG(file)

cfg_start = list(cfg_rules.keys())[0]
     
for i in cfg_rules:
    if(i not in cfg_variables):
        cfg_variables.append(i)

for i in cfg_rules:
    for x in cfg_rules[i]:
        if(x):
            for y in x:
                if(y not in cfg_terminals) and (y not in cfg_variables):
                    cfg_terminals.append(y)

thisCfg = CFG(cfg_terminals, cfg_variables, cfg_rules, cfg_start)
# checks to see if the cfg was gotten correctly
# print(cfg_variables)
# print(cfg_terminals)
# print(cfg_rules)
# print(cfg_start)

derivisions = derive(list(source), list(target))

final_derivisions = []
temp_str = ""
for i in derivisions:
    if(len(i) == 1):
        temp_str += i
    else:
        final_derivisions.append(i)
final_derivisions.append(temp_str)

if derivisions == None:
    print()
else:
    for string in final_derivisions:
        print(string)

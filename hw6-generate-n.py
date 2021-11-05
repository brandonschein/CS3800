import itertools
import sys
import xml.etree.cElementTree as ET
from itertools import combinations 

class CFG:
    def __init__(self, variables, terminals, rules, start):
       self.variables = variables
       self.terminals = terminals
       self.rules = rules
       self.start = start


inputs = sys.stdin.read().split()

file = inputs[0]
num = inputs[1]

cfg_variables = []
cfg_terminals = []
cfg_rules = {}
cfg_start = ""


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


cfg_start = list(cfg_rules.keys())[0]


for i in cfg_rules:
    if(i not in cfg_variables):
        cfg_variables.append(i)

for i in cfg_rules:
    for x in cfg_rules[i]:
        for y in x:
            if(y not in cfg_terminals) and (y not in cfg_variables):
                cfg_terminals.append(y)
        

# print(cfg_variables)
# print(cfg_terminals)
# print(cfg_rules)
# print(cfg_start)

def run_helper(derivations_num, curr):
    if(derivations_num == 0):
        return []
    rights = cfg_rules.get(curr)

    derivations = []

    for right in rights:
        substituted_rights = [[]]
        for char in right:
            if char in cfg_variables:
                if derivations_num == 1:
                    substituted_rights = []
                    break
                substitutions = run_helper(derivations_num - 1, char)

                if (len(substitutions) > 0):
                    new_rights = []
                    for substituted_right in substituted_rights:
                        for sub in substitutions:
                            new_right = substituted_right + sub
                            new_rights.append(new_right)
                    substituted_rights = new_rights
                else:
                    substituted_rights = []
                    break

            else :
                for substituted_right in substituted_rights:
                    substituted_right.append(char)
        derivations += substituted_rights
    
    return derivations

def run(derivations):
    expand = run_helper(derivations, cfg_start)

    return_list = []
    for right in expand:
        right_str = ""
        for char in right:
            right_str += char
        return_list.append(right_str)
    
    return return_list

final_terminals = run(int(num))
for string in final_terminals:
    print(string)


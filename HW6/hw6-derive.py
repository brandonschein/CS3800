import sys
import xml.etree.cElementTree as ET

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
    return CFG(cfg_variables,cfg_terminals,cfg_rules,cfg_start)

inputs = sys.stdin.read().split('\n')

file1 = inputs[0]
source = inputs[1]
target = inputs[2]

cfg = parseCFG(file1)

def terminal_in_start(start, end):
    start_len = len(start)

    for char_s in start:
        if char_s not in cfg.variables:
            if (not char_s in end) and (char_s != ""):
                return False

    return True

def create_variations(current):
    test = current == ["[","S","]"]
    variations = [[]]


    for char in current:

        if char in cfg.variables:
            rights = []
            for i in cfg.rules.get(char):
                newi = i.split()
                rights.append(newi)
    
            #var is invalid
            if rights == None:
                return False

            # Replace the var
            new_variations = []
            for variation in variations:
                for right in rights:
                    #This is for epsilon case
                    if len(right) == 0:
                        right = []
                    new_variations.append(variation + right)

            variations = new_variations


        else:
            for variation in variations:
                variation.append(char)

    return variations


def derive_helper(start, end, visited):
    print(start)
    start_str = ''.join(start)
    #print(start_str)
    if start_str in visited:
        return None

    if len(start) > 1+len(end):
        return None

    visited.add(start_str)

        # match prefix terminals in start with prefix terminals in end
    if not terminal_in_start(start, end):
        return None

    variations = create_variations(start)

    if end in variations:
        return [end]

    for variation in variations:
        ders = derive_helper(variation, end, visited)

        if ders != None:
            return [variation] + ders
    return None

def derive(start, end):
    li = derive_helper(list(start), list(end), set())
    if li == None:
        return None
    ret = []

    for el in li:
        ret.append(''.join(el))
    return [start] + ret
'''
print(cfg.variables)
print(cfg.terminals)
print(cfg.rules)
print(cfg.start)
'''

derivation = derive(source,target)

if derivation == None:
    print()
else:
    for string in derivation:
        print(string)
        
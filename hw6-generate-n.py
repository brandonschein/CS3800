import sys
import xml.etree.cElementTree as ET


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
cfg_rules = []
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
            temp_tuple = []
            for ch in child:
                if(ch.tag == "left"):
                    temp_tuple.append(ch.text)
                if(ch.tag == "right"):
                    temp_tuple.append(ch.text)
                    cfg_rules.append(temp_tuple)

cfg_start = cfg_rules[0][0]

for i in cfg_rules:
    if(i[0] not in cfg_variables):
        cfg_variables.append(i[0])
    for x in i[1]:
        if (x not in cfg_terminals) and not (x.isupper()):
            cfg_terminals.append(x)

print(cfg_variables)
print(cfg_terminals)
print(cfg_rules)
print(cfg_start)

print_array = []
print_array.append(cfg_start)
#preload print_array

# for i in cfg_rules:
#     if(i[0] == cfg_start):
#         print_array.append(i[1])


# def ruleAdvance(arr):
#     new_arr = []
#     for i in arr:
#         temp_arr = []
#         chars = i.split()
#         for x in chars:
#             if(x.isupper()):
#                 for y in cfg_rules:
#                     if(y[0] == x):
#                         temp_arr.append(y[1])
#             else:
#                 temp_arr.append(x)
#         new_arr += temp_arr

#     return new_arr

def ruleAdvance(arr):
    new_arr = []
    for i in arr:
        # design this to be recursive? 
        for x in i:
            temp_str = ""
            if(x.isupper()):
                for y in cfg_rules:
                    if(y[0] == x):
                        temp_str += y[1]
            else:
                temp_str += x
        new_arr.append(temp_str)


for i in range(0, int(num)):
    # print_array += ruleAdvance(print_array)
    print_array.append(ruleAdvance(print_array[len(print_array) - 1]))

    
print(print_array)
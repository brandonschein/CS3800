import sys
import xml.etree.cElementTree as ET

class CFG:
    def __init__(self, variables, terminals, rules, start):
        self.variables = variables
        self.terminals = terminals
        self.rules = rules
        self.start = start

def parse(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    start = ""
    variables = set()
    terminals = set()
    rules = dict()

    chars_in_rules = set()
    for rule in root.findall("./structure/production") + root.findall("./production"):
        left = rule.find('left').text
        right = rule.find('right').text

        variables.add(left)
        right_array = []

        if start == "":
            start = left

        # if right is None, we represent "epsilon" within an empty array
        if right != None:
            for char in right:
                right_array.append(char)
                chars_in_rules.add(char)

        rights = rules.get(left)
        if rights == None:
            rights = []
        rights.append(right_array)
        rules[left] = rights

    # get the set difference which is the terminals
    terminals = list((chars_in_rules - variables))

    return CFG(list(variables), list(terminals), rules, start)

def cfg2xml(cfg):
    top = ET.Element('structure')
    ET.SubElement(top, "type").text = "grammar"

    # start with start
    rights = cfg.rules[cfg.start]
    if rights != None:
        for right_list in rights:
            temp_str = ''
            for r in right_list:
                temp_str += r

            transition_elm = ET.SubElement(top, "production")
            ET.SubElement(transition_elm, "left").text = cfg.start
            ET.SubElement(transition_elm, "right").text = temp_str

    for var in cfg.variables:
        if var != cfg.start:
            rights = cfg.rules[var]
            if rights != None:
                for right_list in rights:
                    temp_str = ''
                    for r in right_list:
                        temp_str += r

                    transition_elm = ET.SubElement(top, "production")
                    ET.SubElement(transition_elm, "left").text = var
                    ET.SubElement(transition_elm, "right").text = temp_str

    tree = ET.ElementTree(top)
    tree.write(sys.stdout, encoding="unicode")
    


def moreNullTransitions(rules, start):
    for var in rules:
        RHS = rules[var]
        for productions in RHS:
            if(len(productions) == 0) and var != start:
                return True
    return False

def CFGtoCNF(cfg):
    vars = cfg.variables
    terminals = cfg.terminals
    start = cfg.start # we are told making the new start case is already done so keep this
    rules = cfg.rules

    # make a simple pass to remove rules that have only V -> ε 
    toRemove = []
    for var in cfg.rules:
        RHS = cfg.rules[var]
        for productions in RHS:
            if(len(productions) == 0) and len(RHS) == 1:
                vars.remove(var)
                toRemove.append(var)
    
    if(len(toRemove) > 0):
        for var in toRemove:
            for v in cfg.rules:
                RHS = cfg.rules[v]
                for productions in RHS:
                    if(var in productions):
                        try:
                            while True:
                                productions.remove(var)
                        except:
                            pass

    
    for key in rules.copy():
        if key in toRemove:
            rules.pop(key)

    # print(vars)
    # print(terminals)
    # print(start)
    # print(rules)

    for var in cfg.rules:
        RHS = cfg.rules[var]
        for production in RHS:
            if(len(production) == 1) and production[0] == var:
                cfg.rules[var].remove(production)

    # print(vars)
    # print(terminals)
    # print(start)
    # print(rules)
     
    # works for grammar5 but gets stuck in grammar4 
    # while(moreNullTransitions(rules, cfg.start)):
    #     # print(rules)
    #     # find a null transition
    #     toRemove = None
    #     for var in rules:
    #         RHS = rules[var]
    #         for productions in RHS:
    #             if(len(productions) == 0):
    #                 toRemove = var
    #     # remove that transition
    #     # print(toRemove)
    #     rules[toRemove].remove([])
    #     # add transitions to where that variable is used in the other productions
    #     for var in rules:
    #         #print(rules)
    #         RHS = rules[var]
    #         for productions in RHS:  
    #             total = sum(s.count(toRemove) for s in productions)
    #             if (total == 1):
    #                 temp_replace = []
    #                 for char in productions:
    #                     if(char != toRemove):
    #                         temp_replace.append(char)
    #                 temp_list = rules[var]
    #                 if(temp_replace not in temp_list):
    #                     temp_list.append(temp_replace)
    #                 rules[var] = temp_list
    #             if(total == 2):
    #                 temp_list = rules[var]
    #                 temp_prod1 = []
    #                 temp_prod2 = []
    #                 for char in productions:
    #                     temp_prod1.append(char)
    #                     temp_prod2.append(char)

    #                 temp_prod1.remove(toRemove)
    #                 temp_list.append(temp_prod1)
                    
    #                 temp_prod2.reverse()
    #                 temp_prod2.remove(toRemove)
    #                 temp_prod2.reverse()
    #                 temp_list.append(temp_prod2)
                    
    #                 rules[var] = temp_list
                               
    return CFG(vars, terminals, rules, start)





#####################################
#main starts here
file = sys.stdin.read()
thiscfg = parse(file)


# print(thiscfg.start) #str
# print(thiscfg.rules) # dict
# print(thiscfg.variables) # list
# print(thiscfg.terminals) # list

#convert to CNF here
newCNF = CFGtoCNF(thiscfg)

# print(newCNF.rules)
# print(newCNF.start)
# print(newCNF.terminals)
# print(newCNF.variables)

cfg2xml(newCNF)

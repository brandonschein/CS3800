import xml.etree.ElementTree as ET
import sys
class CFG:
    def __init__(self, variables, terminals, rules, start):
       self.variables = variables
       self.terminals = terminals
       self.rules = rules
       self.start = start

def derive(start, end):
    ret = []
    for el in derive_helper(start, list(end), []):
        ret.append(''.join(el))
    return [start] + ret

def derive_helper(start, end, visited):
    if start in visited or len(start) > 1+len(end):
        return None

    visited.append(start)

    # match prefix terminals in start with prefix terminals in end
    for char_s in start:
        if char_s not in cfg.variables:
            if (char_s not in end) and (char_s != ""):
                return None

    variations = [[]]

    for char in start:
        if(char):
            if char in cfg.variables:
                rights = cfg.rules[char]

                # Replace the var
                new_variations = []
                for variation in variations:
                    for right in rights:
                        #This is for epsilon case
                        if(right != None and variation != None):
                            if len(right) == 0:
                                right = []
                            new_variations.append(variation + right)

                variations = new_variations

            else:
                for variation in variations:
                    variation.append(char)

    if end in variations: return [end]

    for variation in variations:
        ders = derive_helper(variation, end, visited)

        if ders != None:
            return [variation] + ders
    return None

def parse(filename):
    with open(filename, "r") as file:
        data = ET.parse(file)
        root = data.getroot()

        start = None
        varz = set()
        terms = list()
        rules = dict()

        # go through rules
        all_chars = set()

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
        
        for rule in root.findall("./production"):
            left = rule.find('left').text
            right = rule.find('right').text

            if start == None:
                start = left

            varz.add(left)
            right_array = []

            #if right is None, we represent "epsilon" within an empty array
            if right != None:
                for char in right:
                    right_array.append(char)
                    # keep track of all chars we see
                    all_chars.add(char)

            rights = rules.get(left)
            if rights == None:
                rights = []
            rights.append(right_array)
            rules[left] = rights

        # get the set difference which is the terminals
        terms = list((all_chars - varz))

    return CFG(varz, terms, rules, start)


data = sys.stdin.read()

file, source, target = str(data).split("\n")[:-1]

cfg = parse(file)

# print(cfg.vars)
# print(cfg.terms)
# print(cfg.rules)
# print(cfg.start)

ders = derive(source,target)

if ders == None:
    print()
else:
    for string in ders:
        print(string)

import xml.etree.ElementTree as ET
import sys


class CFG:
    def __init__(self, variables, terminals, rules, start):
        self.variables = variables
        self.terminals = terminals
        self.rules = rules
        self.start = start

#parses xml file and returns CFG
def parse(filename):
    with open(filename, "r") as file:
        tree = ET.parse(file)
        root = tree.getroot()

        variables = set()
        terminals = list()
        rules = {}
        start = ""
        chars = set()

        if root.tag != "structure":
            tag_list = list(root.getchildren())
            pos = 0
            while True:
                if tag_list[pos].tag == "structure":
                    root = tag_list[pos]
                    break
                else:
                    tag_list += list(root.getchildren())
                pos += 1

        for rule in root.findall("./production"):
            left_side = rule.find('left').text
            right_side = rule.find('right').text

            if start == "":
                start = left_side

            variables.add(left_side)
            rightSide = []

            if right_side is not None:
                for char in right_side:
                    rightSide.append(char)
                    chars.add(char)

            new_rights = rules.get(left_side)
            if new_rights is None:
                new_rights = []
            new_rights.append(rightSide)
            rules[left_side] = new_rights

        terminals = list(chars - variables)

    return CFG(variables, terminals, rules, start)

#returns derivision in split string format
def get_derivision(source, target, inspected):
    max_len = len(target)
    max_len += 1
    if source in inspected or len(source) > max_len:
        return None

    inspected.append(source)

    for prefix in source:
        if prefix not in cfg.variables and prefix not in target and prefix != "":
            return None

    vars = [[]]

    for symbol in source:
        if symbol is not None:
            if symbol in cfg.variables:
                all_right = cfg.rules[symbol]

                updated_variations = []
                for variation in vars:
                    for right in all_right:

                        if right is not None and variation is not None:
                            length = len(right)
                            if length < 1:
                                right = []
                            temp = variation + right
                            updated_variations.append(temp)

                vars = updated_variations

            else:
                for variation in vars:
                    variation.append(symbol)

    if target in vars: 
        return [target]

    for variation in vars:
        derives = get_derivision(variation, target, inspected)

        if derives is not None:
            temp = [variation] + derives
            return temp
    return None


#read input
inp = str(sys.stdin.read())

inp = inp.split("\n")
file1 = inp[0]
src = inp[1]
target = list(inp[2])

cfg = parse(file1)

tempList = []
derives = get_derivision(src, target, [])

#condenses output of get_derive into joined string format
for element in derives:
    tempList.append(''.join(element))
derivision = [src] + tempList

if derivision is not None:
    for string in derivision:
        print(string)
else:
    print()
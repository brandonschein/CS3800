import xml.etree.cElementTree as ET
import sys

#class for CFGs, refer to read me for definition
class CFG:
    def __init__(self, variables, terminals, rules, start):
       self.variables = variables
       self.terminals = terminals
       self.rules = rules
       self.start = start

# takes a CFG and prints it out to stdout
def CFGtoXML(cfg):
    root = ET.Element("structure")
    ET.SubElement(root, "type").text = "grammar"

    # load the start terminal first for cfg having the starting terminal first
    rightSide = cfg.rules[cfg.start]
    if(rightSide):
        for list in rightSide:
            right_str = ""
            for prod in list:
                right_str += prod
            cur_production = ET.SubElement(root, "production")

            ET.SubElement(cur_production, "left").text = cfg.start
            ET.SubElement(cur_production, "right").text = right_str
    
    for variable in cfg.variables:
        # make sure that the current variable is not the start variable as that was already loaded
        if (variable != cfg.start):
            rightSide = cfg.rules[variable]
            if (rightSide):
                for list in rightSide:
                    right_str = ""
                    for prod in list:
                        right_str += prod
                    cur_production = ET.SubElement(root, "production")
                    ET.SubElement(cur_production, "left").text = cfg.start
                    ET.SubElement(cur_production, "right").text = right_str
    
    tree = ET.ElementTree(root)
    tree.write(sys.stdout, encoding="unicode")
        

# making the CFG for language L (where L = {w | w = is the string of well-balanced matching brackets})
cfg_variables = ["S"]
cfg_terminals = ["(", ")", "[", "]"]
cfg_rules = {
    "S" : [["[", "S", "]"],
        ["(", "S", ")"],
        ["S", "S"],
        []]
}
cfg_start = "S"

cfgL = CFG(cfg_variables, cfg_terminals, cfg_rules, cfg_start)

CFGtoXML(cfgL)
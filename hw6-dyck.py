import xml.etree.cElementTree as ET
import sys

#CFG definition 

class CFG:
    def __init__(self, variables, terminals, rules, start):
       self.variables = variables
       self.terminals = terminals
       self.rules = rules
       self.start = start

def CFGtoXML(cfg):
    root = ET.Element("structure")
    ET.SubElement(root, "type").text = "grammar"

    # load the start terminal first
    rights = cfg.rules.get(cfg.start)
    if(rights != None):
        for right_list in rights:
            right_str = ""
            for right in right_list:
                right_str += right
            cur_production = ET.SubElement(root, "production")

            
            ET.SubElement(cur_production, "left").text = cfg.start
            ET.SubElement(cur_production, "right").text = right_str
    
    for variable in cfg.variables:
        if (variable != cfg.start):
            rights = cfg.rules.get(variable)
            if (rights != None):
                for right_list in rights:
                    right_str = ""
                    for right in right_list:
                        right_str += right
                    cur_production = ET.SubElement(root, "production")

                    ET.SubElement(cur_production, "left").text = cfg.start
                    ET.SubElement(cur_production, "right").text = right_str
    
    tree = ET.ElementTree(root)
    tree.write(sys.stdout, encoding="unicode")
        

# making the CFG for language L (L = {w | w = is the string of well-balanced matching brackets})
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

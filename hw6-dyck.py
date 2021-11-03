import xml.etree.cElementTree as ET

#CFG definition 

class CFG:
    def __init__(self, variables, terminals, rules, start):
       self.variables = variables
       self.terminals = terminals
       self.rules = rules
       self.start = start

def CFGtoXML(cfg):
    root = ET.Element("structure")

    ET.SubElement(root, "type").text = "grammer"

    for i in cfg.rules:
        cur_production = ET.SubElement(root, "production")

        ET.SubElement(cur_production, "left").text = i[0]
        ET.SubElement(cur_production, "right").text = i[1]

    tree = ET.ElementTree(root)
    tree.write("test.xml")
        

# making the CFG for language L (L = {w | w = is the string of well-balanced matching brackets})
cfg_variables = ["S"]
cfg_terminals = ['(', ')', '[', ']']
cfg_rules = [("S", "[S]"), ("S", "(S)"), ("S", "SS"), ("S", "")]
cfg_start = "S"


cfgL = CFG(cfg_variables, cfg_terminals, cfg_rules, cfg_start)

CFGtoXML(cfgL)

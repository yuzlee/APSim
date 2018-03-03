import xml.etree.cElementTree as ET
from automata_network import  Automatanetwork
import time

def parse_anml_file(file_path):
    start_time = time.time()
    anml_tree = ET.parse(file_path)
    anml_root = anml_tree.getroot()

    if anml_root.tag == 'automata-network':
        automata = Automatanetwork.from_xml(anml_root)
    else:
        automata_network =anml_tree.findall('automata-network')
        assert len(automata_network) == 1
        automata = Automatanetwork.from_xml(automata_network[0])

    print "parsing took:", time.time() - start_time
    return  automata













from __future__ import division
from automata.utility.utility import pact_interconnect
import automata as atma
from automata.AnmalZoo.anml_zoo import anml_path, AnmalZoo
import os
import shutil
from tqdm import tqdm
import numpy as np
import pickle
from automata.utility import utility

routing_template = pact_interconnect()
number_of_automatas = 200
draw_individually = False

report_locs_G4 = set([128 + (i*256) + j for i in range(4) for j in range(8)])

for anml in [AnmalZoo.EntityResolution]:
    automata = atma.parse_anml_file(anml_path[anml])
    automata.remove_ors()
    #utility.minimize_automata(automata)
     # accumulative switch map
    ccs = automata.get_connected_components_as_automatas()

    residual_atms, same_incon_list, curr_node_count, residual_node_count = [], [], 0, 0

    for atm_idx, atm in enumerate(ccs):

        utility.minimize_automata(atm)
        atm.remove_all_start_nodes()

        atm1 = atma.automata_network.get_bit_automaton(atm, original_bit_width=8)
        print "finished bitautomata for %d" % (atm_idx)
        atm4 = atma.automata_network.get_strided_automata2(atm=atm1, stride_value=4, is_scalar=True,
                                                           base_value=2, add_residual=True)
        atm8 = atm4.get_single_stride_graph()

        atm8.make_homogenous()
        print "finished homogeneous for %d" % (atm_idx)

        utility.minimize_automata(atm8)
        print "finished minimizing for %d" % (atm_idx)

        atm8.fix_split_all()
        print "finished splitting for %d" % (atm_idx)

        if curr_node_count + atm8.nodes_count > 1024 or atm is ccs[-1]:

            if curr_node_count + atm8.nodes_count > 1024:
                residual_atms.append(atm8)
                residual_node_count += atm8.nodes_count
            else:
                same_incon_list.append(atm8)
                curr_node_count += atm8.nodes_count

            while same_incon_list:

                print "start placing %d automatas with total nodes %d" % (len(same_incon_list), curr_node_count)
                best_fit = utility.ga_routing(atms_list=same_incon_list,
                                              routing_template=routing_template, available_rows=range(1024),
                                              placement_cond_dic={(temp_atm, temp_node):report_locs_G4 for temp_atm in same_incon_list
                                                                  for temp_node in temp_atm.nodes if temp_node.report},
                                              draw_file='reza{}.png'.format(atm_idx))

                if best_fit != 0:
                    removed_atm = same_incon_list.pop()
                    curr_node_count -= removed_atm.nodes_count
                    residual_atms.append(removed_atm)
                    residual_node_count += removed_atm.nodes_count

                else:
                    same_incon_list, curr_node_count = residual_atms, residual_node_count
                    residual_atms, residual_node_count = [], 0
                    if atm is ccs[-1] and residual_atms:
                        continue
                    else:
                        break

        else:
            same_incon_list.append(atm8)
            curr_node_count += atm8.nodes_count































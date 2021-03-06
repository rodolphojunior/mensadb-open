#!/usr/bin/env python

"""
Deploy vmd to determine interfacial residues of chain B
"""

import vmd
from vmd import molecule
from vmd import evaltcl
import os
import sys

home = os.getcwd()
output_folder = home + "/output"

def detect_chains(input_pdb):

    """
    Detect chains in the pdb input file
    """
    opened_pdb = open(input_pdb, "r").readlines()
    chains = []
    for value in opened_pdb[1:]:
        try:
            if value[21] not in chains:
                chains.append(value[21])
        except:
            continue
    return chains

class interface:


    """
    Interface class object to generate code to run on vmd
    """
    def __init__(self, pdb_path):
        self.input_pdb_path = pdb_path

    def interface_template(self, first_chain = True):

        """
        Define the template to identify residues below 5A interchain distance
        """
        both_chains = detect_chains(self.input_pdb_path)
        if first_chain == True:
            chain_A = both_chains[0]
            chain_B = both_chains[1]
        if first_chain == False:
            chain_A = both_chains[1]
            chain_B = both_chains[0]
        output_string = 'mol new ' + self.input_pdb_path + '\n' \
         + 'set outfile [open ' + output_folder + '/interface_output_B w]' + '\n' \
         + 'set sel1 [atomselect top "protein and (chain ' + chain_A \
         + ') and within 5 of (chain ' + chain_B + ')"]' + '\n' \
         + '$sel1 get {resid resname}' + '\n' \
         + 'set sel2 [lsort -unique [$sel1 get {resid resname}]]' + '\n' \
         + 'puts $outfile "$sel2"' + '\n' \
         + 'close $outfile' + '\n' \
         + 'quit' + '\n' \
         + 'exit' + '\n'
        return output_string


    def generate_interface_temp(self, first_chain = True):

        """
        Write the template file
        """
        output_name = output_folder + "/get_interface.tcl.tpl"
        opened_file = open(output_name, "w")
        writeable_string = interface(self.input_pdb_path).interface_template(first_chain)
        opened_file.write(writeable_string)

    def run_read_output_inter(self):

        """
        Write the output file according to the template measurements
        """
        output_name = "output/interface_output_B"
        evaltcl('play output/get_interface.tcl.tpl')

def run_class_pdb(input_pdb_name):

    """
    Deploy the script
    """    
    interface(input_pdb_name).generate_interface_temp(first_chain = False)
    interface_chain = interface(input_pdb_name).run_read_output_inter()

home = os.getcwd()
input_file = home + "/" + sys.argv[1]
run_class_pdb(input_file)


"""
This file contains shared functions for the project

@author: VT Ni-Lab
"""
import os, csv

# Parse input CSV file to get list of parameters
def parse_file(infile):
    param_list = None
    # check if the infile exists
    if not os.path.exists(infile):
        print("Parameter file is not exist: ", infile)
    else:
        print("parsing parameter file: ", infile)
        with open(infile, newline='') as f:
            reader = csv.reader(f, delimiter=',')
            param_list = list(reader)[1]
        print(param_list)
    return param_list

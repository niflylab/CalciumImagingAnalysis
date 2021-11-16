#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 14:23:31 2021
This file conducts Calcium Imaging analyses such as fluorescence extraction analysis and plotting.
It uses 3 functions fluorescence_extract(), loop_fluorescence_extract(), and merge_data() imported from other scripts individual_dFoverF0_1.py and merge_dFoverF0_1.py

Usage: CIAnalysis.py -i <project_dir> [-t <number of position t>] [-b <background_file>] [-merge] [--help]

@author: VT Ni-Lab
"""

import os
import sys, argparse
from utility import parse_file
from individual_dFoverF0_1 import loop_fluorescence_extract
from merge_dFoverF0_1 import merge_data

def main():
    # set default project directory as current script path
    project_dir = os.getcwd()

    # initialize argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--project_dir', type=str, required=False, help='Project directory to do analysis')
    # add -t to allow user input their t value
    parser.add_argument('-t', '--position_t', type=int, required=False, default=100, help='number of position t')
    parser.add_argument('-b', '--background_file', type=str, required=False, help='Background list file path')
    parser.add_argument('-merge', '--merge', type=int, required=False, help='Merge extracted data', nargs='?', const=1)

    args = parser.parse_args()

    #Prompt user if project directory is not specified in commandline
    if args.project_dir is None:
        print("project directory is not specified, use current directory? (y/n) ")
        choice = input().lower()
        if choice not in ("y", "yes", ""):
            parser.print_help()
            print("Please type project directory, then press ENTER ...")
            project_dir = input().strip()
    else:
        project_dir = args.project_dir.strip()

    if args.background_file is not None:
        background_file = args.background_file.strip()

    # init default paths for file and folder
    analysis_dir = os.path.join(project_dir)
    results_dir = os.path.join(analysis_dir, "results")
    background_file = os.path.join(analysis_dir, "Background_list.csv")
    number_of_position_t = 100
    plot_title = "Average \u0394F/F0"
    merge = args.merge

    # check file or folder existence
    for path in (project_dir, analysis_dir, background_file):
        if not os.path.exists(path):
            print("Path does not exist: ", path)
            sys.exit(1)
    print(
        "Running CIAnalysis with settings: \n --Project Folder: {0} \n --Position t: {1} \n --Background List: {2} \n --Merge result data is {3}".format(
            project_dir, number_of_position_t, background_file, str(merge)))

    # Step 1: loop_fluorescence_extract
    # Parse parameter csv file to get position_t value
    # param_list = parse_file(param_file)

    if args.position_t is not None:
        number_of_position_t = int(args.position_t)
        # execute the loop_fluorescence_extract
        print("Processing fluorescence extraction...")
        loop_fluorescence_extract(analysis_dir, background_file, number_of_position_t, results_dir)
        print('merge: ', merge)
        # Step 2: merge_data
        if merge is not None:
            # check fluorescence_extract results
            if not os.path.exists(results_dir) or not os.listdir(results_dir):
                print("Fluorescence extraction results are not found")
                sys.exit()
            else:
                print("Merging data...")
                merge_data(results_dir, number_of_position_t, plot_title)

if __name__ == "__main__":
    main()

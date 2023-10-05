#!/usr/bin/env python
# coding: utf-8

# Permutation Tests For NCI-MATCH Basket Trials
# ===
# Created 8/14/22
# Edited 10/3/23, 10/4

import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import math

import functions_permutation_test

# Names of drugs tested and corresponding NCI MATCH subprotocols
# Ambiguity in Copanlisib trial: one point unknown cancer type, but narrowed down to GI or Gyn
info = [["Dabrafenib&Trametinib", "H"],
       ["T-DM1", "Q"],
       ["Trametinib","R"],
       ["Nivolumab", "Z1D"],
       ["AZD4547", "W"],
       ["Capivasertib", "Y"],
       ["Binimetinib", "Z1A"],
       ["Taselisib", "I"],
       ["CopanlisibBlank", "Z1F"],
       ["Afatinib", "B"]]

data_folder = "./data/original/"
samp_folder = "./output/sampled data/"
plot_folder = "./output/plots/"
out_folder = "./output/"

############################################
# examples:                                #
# permutation_test_forcluster.py 0 5 1 pfs #
#     use the 0th trial, 10^5 times, 1st   #
#     iteration, sample pfs                #
# permutation_test_forcluster.py 2 7 9 tvc #
#     use the 3rd trial, 10^7 times, 9th   #
#     iteration, sample tvc                #
############################################
import time
import sys
if __name__ == "__main__":
    i = int(sys.argv[1])
    it = int(sys.argv[2])
    n_it = sys.argv[3]
    type = sys.argv[4]
    if type == "pfs":
        fileloc = data_folder + str(i+1) + "_" + info[i][1] + "_pfs.xlsx"
        print(fileloc)
        df = pd.read_excel(fileloc, engine='openpyxl')
        if i == 3 or i == 5:
            aggby = "Cancer category"
        else:
            aggby = "Cancer type"
        
        typecount = count_types(df, by=aggby, mode="Months")
        values = df.iloc[:,-2:]
        start = time.time()
        sampled = sample_pfs(typecount, values, 10**it)
        sampled.to_csv(samp_folder + str(i+1) + "_" + info[i][1] + "_pfs.xlsx" + aggby + ".sampled_it"+n_it +".csv")
        print("Done! in", (time.time()-start) / 3600, "hours!")


    elif type == "tvc":
        fileloc = data_folder + str(i+1) + "_" + info[i][1] + "_tumorchange.xlsx"
        print(fileloc)
        df = pd.read_excel(fileloc, engine='openpyxl')
    
        if i == 3 or i == 5:
            aggby = "Cancer category"
        else:
            aggby = "Cancer type"
    
        typecount = count_types(df, by=aggby)
        values = df.iloc[:,-2]
    
        # Start timing
        start = time.time()
        sampled = sample(typecount, values, it=10**it)
        sampled.to_csv(samp_folder + str(i+1) + "_" + info[i][1] + "_tumorchange.xlsx" + aggby + ".sampled_it"+n_it +".csv")
        print("Done! in", (time.time()-start) / 3600, "hours!")
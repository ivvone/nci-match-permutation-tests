#!/bin/bash

#SBATCH --ntasks=1
#SBATCH --time=20:00:00
#SBATCH --mem=4g

# i = 8
# 10^7
# iteration 1
# pfs

python3 run_permutation_test.py 4 7 1 tvc

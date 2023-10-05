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

def count_types(df, by, mode="Percent change"):
    """Returns # in each subtype, in descending order
    
    df = DataFrame containing the column of subtypes
    by = name of column containing subtypes
    mode = the values measured"""
    typecount = df.groupby(by=by).agg('count')
    typecount.sort_values(by=[mode], inplace=True, ascending=False)
    typecount = typecount[mode]
    return typecount


def p_calc(subtype_avg, x):
    """Returns left, right p-values
    
    subtype average= mean tumor volume change for that cancer type
    x= list of observations in null distribution (average tumor volume change for every iteration of simulation)"""
    left = sum(x <= subtype_avg) / len(x) #corresponds to test for superior tumor shrinkage
    right = sum(x >= subtype_avg) / len(x)  #corresponds to test for inferior tumor shrinkage
    return left, right


# ## 3. Tumor Volume Change

def sample(typecount, values, it=1000):
    """Returns df of subtype sampling (n>2)
    
    values = all tumor volume changes in a trial 
    typecount = number of patient for subgroup of interest 
    it = number of simulations to construct null hypothesis""" 
    names = typecount.index
    df_tosave = pd.DataFrame(columns=names)
    
    for i in range(len(typecount)):
        n = typecount[i]
        if n < 3 or names[i] == "Other":
            continue
        x = [np.average(values.sample(int(n))) for j in range(it)]
        df_tosave[names[i]] = x
    return df_tosave

# ## 3. Progression-Free Survival

from lifelines import CoxPHFitter
from lifelines import KaplanMeierFitter
import random
import math

def sample_pfs(typecount, values, it=1000):
    names = typecount.index
    df_tosave = pd.DataFrame(columns=names)
    
    for i in range(len(typecount)):
        n = typecount[i]
        if n < 3:
            continue
        x = [calc_hazard_ratio(values, values.shape[0], n) for j in range(it)]
        df_tosave[names[i]] = x
    return df_tosave

def calc_hazard_ratio(df, length, n):
    # Process df for analysis
    new_df = df
    subset_col = [0] * length + [1] * n
    new_df = new_df.append(new_df.sample(n))
    new_df["Subset"] = subset_col
    new_df = new_df[["Months", "Censoring value", "Subset"]]
    
    # Fit
    cph = CoxPHFitter()
    cph.fit(new_df, duration_col="Months", event_col="Censoring value")
    
    # Hazard ratio
    ratio = cph.hazard_ratios_["Subset"]
    #print(cph.confidence_intervals_)
    #cph.plot()
    
    return ratio


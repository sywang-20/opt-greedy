# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 13:16:56 2023

@author: yulun
"""

# run 20 cases same parameter

from main import run_case

from multiprocessing import Pool
import os, time, random
import numpy as np
import pandas as pd
#from multiprocessing import get_context


def run_case_cp_mp(cp, mp):
    print('------- Running CP:{:.2f}, MP:{:.2f}'.format(cp, mp))
    
    start = time.time()    
    
    run_case(cp=cp, mp=mp)
    
    end = time.time()
    t = end - start

    return [mp, cp, t] # return a log


if __name__ == '__main__':
    mps = np.linspace(0,0.5,6)
    cps = np.linspace(0,1,11)
    print(mps, cps)
    
    t = [(cpi, mpi) for cpi in cps for mpi in mps]

    
    cpu_count = os.cpu_count()
    with Pool(cpu_count - 1) as p:
         msgs = p.starmap(run_case_cp_mp, t)
 
    M = pd.DataFrame(msgs, columns=['mp', 'cp', 't'])
    M.to_csv('./log_grid_mp_cp.csv', index=False)
    
# >> no print outs 
# >> progress monitoring
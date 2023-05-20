# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 14:40:43 2023

@author: yulun
"""

from utils_common import read_pkl
import numpy as np
from pathlib2 import Path
import pygmo


def load_best_greedy(mode='obj'):
    '''
    load solution or objective values of the best results from greedy algorithm. 

    Parameters
    ----------
    mode : TYPE, ['obj', '']
        DESCRIPTION. The default is 'obj'.

    Returns
    -------
    D : TYPE
        DESCRIPTION. 'obj' to get objective values. '' to get the solution object.
    '''
    project_path= Path(r"C:\Users\yulun\Desktop\r-SPO-230110\HV-code")  # CZ: absolute address to be updated
    fn_solution = project_path/'solution-best-greedy-iter_100_Lmax_200_new_plans_10.pkl'
    D = read_pkl(fn_solution)
    
    if mode == 'obj':
        D = solution_to_objective_values(D)    
    return D




# extract objective values from solution
def solution_to_objective_values(solution):
    objective_values = []
    for i in range(len(solution)): 
        individuals = solution[i]
        objective_values.extend([[i] + individual[:3] for individual in individuals])
    objective_values = np.array(objective_values)
    print('Extracted {} chromosomes in {} iterations.\nThe first column is iteration number. The rest are raw objective values.'.format(len(objective_values), len(solution)))
    return objective_values

#objective_values = solution_to_objective_values(solution)


def calc_HV(objective_values, norm=True, ref_point=[1,1,1], columns=['cost', 'coverage', 'resolution']):
    '''
    calculate Hypervolumn value for objective values. 

    Parameters
    ----------
    objective_values : TYPE np.array
        DESCRIPTION.
    norm : TYPE, boolean
        DESCRIPTION. Whether to normalize objective values. The default is True. 
    ref_point : TYPE, list
        DESCRIPTION. The default is [1,1.01,1].
    columns : TYPE, list
        DESCRIPTION. Column names respectively for objective values. Need to be consistent with keys in norm_params. The default is ['cost', 'coverage', 'resolution'].

    Returns
    -------
    hv, TYPE float
        DESCRIPTION. 

    '''
    def normalize_objective_values(objective_values):
        
        def load_norm_params():
            project_path= Path(r"D:/project/SPO")  # >> absolute address to be updated
            D = read_pkl(project_path/'norm_para_413.pkl')
            print('- Loaded norm params as a dict().\n-- Key: objective name\n-- Value: [min, max]')
            return D        
        
        def normalize(values, norm_params, col):
            mini, maxi = norm_params[col]
            return (values - mini)/(maxi - mini)
        
        norm_params = load_norm_params()
        
        objective_values_norm = objective_values.copy()
        for i in range(3):
            objective_values_norm[:, i] = normalize(objective_values[:, i], norm_params, columns[i])
        return objective_values_norm
    
    if norm == True:
        print('Normalization applied.')
        objective_values_norm = normalize_objective_values(objective_values)
    else:
        print('Un-normalized. Make sure the input is normalized.')
        objective_values_norm = objective_values
    hv = pygmo.hypervolume(objective_values_norm).compute(ref_point)
    return hv



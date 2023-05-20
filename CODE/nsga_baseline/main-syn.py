import matplotlib.pyplot as plt
import networkx as nx
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math
# from nsga.evolution import Evolution
# from nsga.problem import Problem
from evolution import Evolution
from problem import Problem
# from nsga import precomputation
# from nsga import objective
#import precomputation
import objective
import math
import pickle
import argparse
import os

# def create_conn_dict(G):
#     n = len(G)
#     conn_dict = dict()
#
#     for node_i in range(n):
#         print(node_i)
#         for node_j in range(n):
#             if nx.has_path(G, node_i, node_j):
#                 conn_dict[(node_i,node_j)] = 1
#     return conn_dict
'''
对synthetic case进行计算
'''

if __name__=='__main__':
    parser = argparse.ArgumentParser(usage="it's usage tip.", description="help info.")

    # 需要用的参数都直接修改default，只留一个size
    parser.add_argument("--mp", type=float,default=0.05, help="the mutation param")
    parser.add_argument("--cp", type=float,default=0.8, help="the crossover param")
    parser.add_argument("--iter", type=int, default=1000,  help="the iteration number")
    parser.add_argument("--size", type=int, default=30,help="synthetic case size")
    parser.add_argument("--cc", type=float, default=0, help="coverage constraint")
    # parser.add_argument("--gen", type=int, default=100, required=True, help="the sensor upbound")
    # parser.add_argument("--upbound", type=int, default=100,  help="the sensor upbound")

    args = parser.parse_args()

    mp=args.mp
    cp=args.cp
    iter=args.iter
    coverage_constrain = args.cc
    size=args.size
    upbound=int(size/10)

    case_dir="../../DATA/synthetic_network/"+str(size)+"/"
    # 数一下这个size下有多少个不同网络
    count = 0
    for file in os.listdir(case_dir):  # file 表示的是文件名
        count += 1

    for i in range(count):
        print('begin read data')
        sol_dir= '../../TESTOUTPUT/synthetic_simulation/'+str(size)+'/'+str(i)
        if os.path.exists(sol_dir):
            continue

        with open(case_dir+str(i)+"/prepared-new/upstream_set.pkl", "rb") as tf:
            upstream_set = pickle.load(tf)
        tf.close()

        with open(case_dir+str(i)+"/prepared-new/upstream_arr.pkl", "rb") as tf:
            upstream_arr = pickle.load(tf)
        tf.close()

        fn = case_dir+str(i)+"/prepared-new/syn.pkl"
        relabeled_G = nx.read_gpickle(fn)
        node_num = len(relabeled_G.nodes())
        print(node_num)

        with open(case_dir+str(i)+"/prepared-new/conn_dict.pkl", "rb") as tf:
            conn_dict = pickle.load(tf)
        tf.close()

        sample=np.ones(len(upstream_arr))

        problem = Problem(objectives=[objective.sensor_num,objective.coverage,objective.final_edition_search_cost], node_num=node_num, upstream_arr=upstream_arr,
                         coverage_constrain=coverage_constrain,upstream_set=upstream_set,sensor_upbound=upbound,graph=relabeled_G,priority=sample,conn_dict=conn_dict)

        fig_path = '../../TESTOUTPUT/synthetic_simulation_no_dup/'+str(size)+'/'+str(i)+'/gen_' + str(iter) + '_mp_' + str(mp) + '_cp_' + str(cp) +'_up_'+str(upbound) + '_cc' + str(coverage_constrain) +'/'
        # fig_path='./diversitytest/'
        if not os.path.exists(fig_path):
            os.makedirs(fig_path)
        suffix=0
        for file in os.listdir(fig_path):
            suffix+=1
        fig_path=fig_path+"/"+str(suffix)+"/"
        print('test')
        # fig_path="E:/Study/HKU/docu for the draft/result_analysis/constrain_result/"+str(iter)+'_m'+str(mp)+'_c'+str(cp)+'_up'+str(upbound)+'/'
        evo = Evolution(problem, num_of_generations=iter, num_of_individuals=200, num_of_tour_particips=2, tournament_prob=0.8,
                                crossover_param=cp, mutation_param=mp,fig_path=fig_path,node_num=node_num)

        solution = evo.evolve()
        goals = [i.objectives for i in solution]

        coverage_goal = [i[0] for i in goals]
        sensor_num_goal = [i[1] for i in goals]
        search_cost_goal = [i[2] for i in goals]

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
import constraint
import time

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
    # 每一步增加的sensor数量不能少于保留的plan数量
    parser = argparse.ArgumentParser(usage="it's usage tip.", description="help info.")
    parser.add_argument("--iter", type=int, default=5, help="the iteration number")  # 迭代次数，sensor number的upper bound
    parser.add_argument("--num_of_individual", type=int, default=10, help="the number of reserved plans in each step")
    parser.add_argument("--new_plans", type=int, default=2, help="the number of new plans generated from one sensor")
    parser.add_argument("--datadir", type=str, default="../../../DATA/real_life_case_network/data/")  # 对应网络数据的保存目录
    parser.add_argument("--outdir", type=str,
                        default="../../../TESTOUTPUT/local_search/greedy_nondominated_parameter_latest/")  # 对应输出结果的保存目录
    parser.add_argument("--size", type=int, default=100, help="the size of the network")
    # parser.add_argument("--gen", type=int, default=100, required=True, help="the sensor upbound")
    # parser.add_argument("--upbound", type=int, default=100,  help="the sensor upbound")

    args = parser.parse_args()

    # 读取前面的各类参数
    #search_steps = args.iter
    output_dir = args.outdir
    parent_dir = args.datadir
    num_of_individuals = args.num_of_individual
    new_plans_num = args.new_plans
    size= args.size
    search_steps=int(size/10)

    case_dir="../../DATA/synthetic_network/"+str(size)+"/"
    # 数一下这个size下有多少个不同网络
    # count = 0
    # for file in os.listdir(case_dir):  # file 表示的是文件名
    #     count += 1


    for i in [0]: #range(count):
    #for i in range(count):
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

        problem = Problem(objectives=[objective.coverage,objective.new_search_cost_by_topology_2], constraint=[constraint.sensor_num],node_num=node_num, upstream_arr=upstream_arr,
                         upstream_set=upstream_set,graph=relabeled_G,conn_dict=conn_dict)

        fig_path = '../../TESTOUTPUT/synthetic_simulation/greedy_evo/'+str(size)+'/'+str(i)+'/'

        if not os.path.exists(fig_path):
            os.makedirs(fig_path)
        suffix=0
        for file in os.listdir(fig_path):
            suffix+=1
        fig_path=fig_path+str(suffix)


        # fig_path="E:/Study/HKU/docu for the draft/result_analysis/constrain_result/"+str(iter)+'_m'+str(mp)+'_c'+str(cp)+'_up'+str(upbound)+'/'
        evo = Evolution(problem, search_steps=search_steps, num_of_individuals=num_of_individuals,new_plans_num=new_plans_num, fig_path=fig_path, node_num=node_num)

        print("start")
        start=time.time()
        solution = evo.evolve()
        end=time.time()

        with open(os.path.join(fig_path, "time.txt"), "w") as tf:
            tf.write(str(end - start))

        # goals = [i.objectives for i in solution]
        #
        # coverage_goal = [i[0] for i in goals]
        # sensor_num_goal = [i[1] for i in goals]
        # search_cost_goal = [i[2] for i in goals]
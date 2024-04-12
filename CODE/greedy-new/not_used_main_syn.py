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

'''
对synthetic case进行计算
'''
def run_case(size):
    case_dir = "../../DATA/synthetic_network/" + str(size) + "/"
    # 数一下这个size下有多少个不同网络
    max_sensor=int(size/10)
    num_of_individuals=20
    count = 0
    for file in os.listdir(case_dir):  # file 表示的是文件名
        count += 1

    for i in range(count):
        sol_dir = '../../TESTOUTPUT/synthetic_simulation/' + str(size) + '/' + str(i)
        if os.path.exists(sol_dir):
            continue

        with open(case_dir + str(i) + "/prepared-new/upstream_set.pkl", "rb") as tf:
            upstream_set = pickle.load(tf)
        tf.close()

        with open(case_dir + str(i) + "/prepared-new/upstream_arr.pkl", "rb") as tf:
            upstream_arr = pickle.load(tf)
        tf.close()

        fn = case_dir + str(i) + "/prepared-new/syn.pkl"
        relabeled_G = nx.read_gpickle(fn)
        node_num = len(relabeled_G.nodes())
        print(node_num)

        with open(case_dir + str(i) + "/prepared-new/conn_dict.pkl", "rb") as tf:
            conn_dict = pickle.load(tf)
        tf.close()

        sample = np.ones(len(upstream_arr))

        problem = Problem(objectives=[objective.coverage, objective.search_cost],
                          constraint=[constraint.sensor_num], node_num=node_num, upstream_arr=upstream_arr,
                          upstream_set=upstream_set, graph=relabeled_G, conn_dict=conn_dict)

        fig_path = '../../TESTOUTPUT/synthetic_simulation/greedy_original/' + str(size) + '/' + str(i) + '/'

        if not os.path.exists(fig_path):
            os.makedirs(fig_path)
        suffix = 0
        for file in os.listdir(fig_path):
            suffix += 1
        fig_path = fig_path + str(suffix)

        # fig_path="E:/Study/HKU/docu for the draft/result_analysis/constrain_result/"+str(max_sensor)+'_m'+str(mp)+'_c'+str(cp)+'_up'+str(upbound)+'/'
        evo = Evolution(problem, max_sensor=max_sensor, num_of_individuals=num_of_individuals, fig_path=fig_path,
                        node_num=node_num)

        print("start")
        start = time.time()
        solution = evo.evolve()
        end = time.time()

        with open(os.path.join(fig_path, "time.txt"), "w") as tf:
            tf.write(str(end - start))

if __name__=='__main__':
    parser = argparse.ArgumentParser(usage="it's usage tip.", description="help info.")

    # 需要用的参数都直接修改default，只留一个size
    parser = argparse.ArgumentParser(usage="it's usage tip.", description="help info.")
    #parser.add_argument("--max_sensor", type=int, default=5, help="upper bound of the number of sensors")  # sensor number的upper bound
    parser.add_argument("--num_of_individual", type=int, default=10, help="the number of reserved plans in each step")
    parser.add_argument("--size", type=int, default=100, help="the size of the network")


    args = parser.parse_args()

    # 读取前面的各类参数
    #max_sensor = args.max_sensor
    #output_dir = args.outdir
    #parent_dir = args.datadir
    num_of_individuals = args.num_of_individual
    size= args.size
    max_sensor=int(size/10)

    run_case(max_sensor, num_of_individuals, size)



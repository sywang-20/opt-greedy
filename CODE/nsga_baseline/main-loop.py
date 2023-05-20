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
# import precomputation
import objective
import math
import pickle
import argparse
import os
import time
'''
通过循环，重复多次实验
--mp 对应mutation parameter
--cp 对应crossover parameter
--iter 对应NSGA算法的迭代次数
--upbound对应sensor number的上界
--cc用于限制新生成的individual的coverage，新生成的individual coverage>=total coverage *cc
--netdir 对应网络数据文件目录
--outdir simulation结果的输出目录
'''


def pre_read(parent_dir="../../DATA/real_life_case_network/"):
    # 读取各种需要的数据
    # with open("../prepared/upstream_set.pkl", "rb") as tf:
    with open(parent_dir+"prepared/upstream_set.pkl","rb") as tf:
        # 上游node的集合
        upstream_set = pickle.load(tf)
    tf.close()

    # with open("../prepared/upstream_arr.pkl", "rb") as tf:
    with open(parent_dir+"prepared/upstream_arr.pkl","rb") as tf:
        # 上游node个数
        upstream_arr = pickle.load(tf)
    tf.close()

    # fn = '../prepared/pipe_TM_clean_relabel.pkl'
    fn=parent_dir+"prepared/pipe_TM_clean_relabel.pkl"

    relabeled_G = nx.read_gpickle(fn)
    node_num = len(relabeled_G.nodes())
    print(node_num)

    with open(parent_dir+"prepared/conn_dict.pkl", "rb") as tf:
        conn_dict = pickle.load(tf)
    tf.close()

    return upstream_arr, upstream_set,relabeled_G,conn_dict,node_num


if __name__=='__main__':
    # 创建一个ArgumentParser对象
    parser = argparse.ArgumentParser(usage="it's usage tip.", description="help info.")

    # 添加参数
    parser.add_argument("--mp", type=float,default=0.05, help="the mutation param")
    parser.add_argument("--cp", type=float,default=0.8, help="the crossover param")
    parser.add_argument("--iter", type=int, default=5,  help="the iteration number")
    parser.add_argument("--cc",type=float,default=0,help="coverage constraint")
    parser.add_argument("--upbound", type=int, default=100,  help="the sensor upbound")
    parser.add_argument("--netdir",type=str, default="../../DATA/real_life_case_network/",help="The directory of preprocessed network data")
    parser.add_argument("--outdir",type=str,default="../../TESTOUTPUT/real_life_case_nsga/",help="The directory of results")  #这里定义输出结果保存的路径
    # 解析参数
    args = parser.parse_args()

    mp=args.mp
    cp=args.cp
    gen_num=args.iter
    coverage_constrain=args.cc
    sensor_upbound=args.upbound
    network_dir=args.netdir
    output_dir=args.outdir

    # 调用pre_read读取需要的数据
    upstream_arr, upstream_set, relabeled_G, conn_dict, node_num=pre_read(parent_dir=network_dir)

    # 例子：所有元素都为 1
    sample=np.ones(len(upstream_arr))
    start = time.time()

    for i in range(10):
        problem = Problem(objectives=[objective.sensor_num, objective.coverage, objective.final_edition_search_cost],
                          node_num=node_num, upstream_arr=upstream_arr,
                          upstream_set=upstream_set, sensor_upbound=sensor_upbound,
                          coverage_constrain=coverage_constrain, graph=relabeled_G, priority=sample,
                          conn_dict=conn_dict)

        fig_path = os.path.join(output_dir, 'gen_' + str(gen_num) + '_mp' + str(mp) + '_cp' + str(cp) + '_up' + str(
            sensor_upbound) + '_cc' + str(coverage_constrain) + '/')

        if not os.path.exists(fig_path):
            os.makedirs(fig_path)
        cnt = len(os.listdir(fig_path))
        fig_path = os.path.join(fig_path, str(cnt))

        evo = Evolution(problem, num_of_generations=gen_num, num_of_individuals=200, num_of_tour_particips=2,
                        tournament_prob=0.8,
                        crossover_param=cp, mutation_param=mp, fig_path=fig_path)

        solution = evo.evolve()

    end = time.time()
    print("execution time: " + str(end - start))


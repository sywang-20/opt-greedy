import pickle
import networkx as nx
import numpy as np
import argparse
import os
from evolution import Evolution  # control the iterative process of NSGA-II
from problem import Problem  # 构建problem
import objective  # 目标函数的计算
import individual
import time

'''
multi-objective greedy algorithm for real-life-case
每一步都考虑前一步的parent，基于objective value进行sorting，只有有提升才update solution
'''
# 读取处理过后的data
def pre_read_real(parent_dir):
    with open(parent_dir + "/prepared/upstream_set.pkl", "rb") as tf:
        upstream_set = pickle.load(tf)
    tf.close()

    with open(os.path.join(parent_dir, "prepared/upstream_arr.pkl"), "rb") as tf:
        upstream_arr = pickle.load(tf)
    tf.close()

    fn = os.path.join(parent_dir, "prepared/pipe_TM_clean_relabel.pkl")
    relabeled_G = nx.read_gpickle(fn)
    node_num = len(relabeled_G.nodes())
    print(node_num)

    with open(os.path.join(parent_dir, "prepared/conn_dict.pkl"), "rb") as tf:
        conn_dict = pickle.load(tf)
    tf.close()

    return upstream_set, upstream_arr, relabeled_G, node_num, conn_dict


if __name__ == '__main__':

    """
    PARAMETER INITIALIZATION，设置各类参数
    --iter 每次placement中sensor总数的上限
    --num_of_individual 每个iteration保留多少个solution
    --new_plans 每个solution会生成多少个新的solution
    --datadir 对应网络数据文件目录
    --outdir simulation结果的输出目录
    """
    parser = argparse.ArgumentParser(usage="it's usage tip.", description="help info.")
    parser.add_argument("--iter", type=int, default=5, help="the iteration number")  # 迭代次数，sensor number的upper bound
    parser.add_argument("--num_of_individual", type=int, default=10, help="the number of reserved plans in each step")
    parser.add_argument("--new_plans", type=int, default=20, help="the number of new plans generated from one sensor")
    parser.add_argument("--datadir", type=str, default="../../../DATA/real_life_case_network/data/")  # 对应网络数据的保存目录
    parser.add_argument("--outdir", type=str,
                        default="../../../TESTOUTPUT/local_search/greedy/")  # 对应输出结果的保存目录

    args = parser.parse_args()

    # 读取前面的各类参数
    search_steps = args.iter
    output_dir = args.outdir
    parent_dir = args.datadir
    num_of_individuals = args.num_of_individual
    new_plans_num = args.new_plans

    upstream_set, upstream_arr, relabeled_G, node_num, conn_dict = pre_read_real(parent_dir)


    start=time.time()
    fig_path = os.path.join(output_dir, 'iter_' + str(search_steps) + '_Lmax_' + str(num_of_individuals) + '_new_plans_' + str(new_plans_num) + '/')

    # 根据输出数据目录是否存在，创建目录
    if not os.path.exists(fig_path):
        os.makedirs(fig_path)
        print('create directory successfully')
    cnt = len(os.listdir(fig_path))

    fig_path = fig_path + str(cnt)
    if not os.path.exists(fig_path):
        os.makedirs(fig_path)

    priority = np.ones(node_num)
    for i in range(10):
        problem = Problem(objectives=[objective.sensor_num, objective.coverage, objective.new_search_cost_by_topology_2],
                          node_num=node_num, upstream_arr=upstream_arr,  upstream_set=upstream_set,  graph=relabeled_G,
                         conn_dict=conn_dict)

        evo = Evolution(problem, search_steps=search_steps, num_of_individuals=num_of_individuals,
                        new_plans_num=new_plans_num, fig_path=fig_path)

        evo.evolve()

    end=time.time()
    print("execution time: "+ str(end-start))
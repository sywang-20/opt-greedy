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
import constraint
'''
multi-objective greedy algorithm for real-life-case
每一步都考虑前一步的parent，有提升才update solution
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
    --case 对应real-life or synthetic case
    --datadir 对应网络数据文件目录
    --outdir simulation结果的输出目录
    """
    parser = argparse.ArgumentParser(usage="it's usage tip.", description="help info.")
    parser.add_argument("--iter", type=int, default=5, help="the iteration number")  # 迭代次数，sensor number的upper bound
    parser.add_argument("--num_of_individual", type=int, default=10, help="the number of reserved plans in each step")
    #parser.add_argument("--new_plans", type=int, default=20, help="the number of new plans generated from one sensor")
    parser.add_argument("--datadir", type=str, default="../../DATA/real_life_case_network/data/")  # 对应网络数据的保存目录
    parser.add_argument("--outdir", type=str,
                        default="../../TESTOUTPUT/local_search/greedy_original/")  # 对应输出结果的保存目录
    # parser.add_argument("--coverage", type=int, default=500, help="maximum coverage increment")
    # parser.add_argument("--searchcost", type=float, default=0.01, help="maximum search cost")
    # parser.add_argument("--plans_num_per", type=int, default=20, help="the number of reserved new plans generated from one sensor")

    args = parser.parse_args()

    # 读取前面的各类参数
    search_steps = args.iter
    output_dir = args.outdir
    parent_dir = args.datadir
    num_of_individuals = args.num_of_individual
    #new_plans_num = args.new_plans
    #plans_num_per=args.plans_num_per
    # coverage_increment_max = args.coverage
    # search_cost_increment_max = args.searchcost
    # sensor_upbound = args.upbound
    # sensor_lowbound = args.lowbound

    # upstream_set, upstream_arr, relabeled_G, node_num, conn_dict=pre_read_syn()


    upstream_set, upstream_arr, relabeled_G, node_num, conn_dict = pre_read_real(parent_dir)


    start=time.time()
    #通过循环进行多次计算
    #for i in range(10):
    #fig_path = os.path.join(output_dir,'iter_' + str(search_steps) +'_coverage_' + str(coverage_increment_max) +'_search_cost_' + str(search_cost_increment_max) +'_Lmax_' + str(num_of_individuals) + '_new_plans_' + str(new_plans_num) + '/')
    fig_path = os.path.join(output_dir, 'iter_' + str(search_steps) + '_Lmax_' + str(num_of_individuals) + '_new_plans' + '/')

    # 根据输出数据目录是否存在，创建目录
    if not os.path.exists(fig_path):
        os.makedirs(fig_path)
        print('create directory successfully')
    cnt = len(os.listdir(fig_path))

    fig_path = fig_path + str(cnt)
    if not os.path.exists(fig_path):
        os.makedirs(fig_path)

    # 每个manhole的优先级，在当前case中都是一样的，所以全部设置为1，不需要管
    priority = np.ones(node_num)

    # Describes important constraints in the simulation implementation.构建这么一个多目标优化的问题，用于后续使用evo进行求解
    problem = Problem(objectives=[objective.coverage, objective.new_search_cost_by_topology_2],
                      constraint=[constraint.sensor_num],
                      # 目标函数
                      node_num=node_num, upstream_arr=upstream_arr,  # 限制条件以及一些需要的数据
                      upstream_set=upstream_set,  # sensor_upbound=sensor_upbound,sensor_lowbound=10,
                      graph=relabeled_G,
                      conn_dict=conn_dict)

    # controls the iterative process of NSGA-II. evolution函数对上面构建的problem进行求解-->需要修改算法的话，应该主要修改evolution里的东西
    evo = Evolution(problem, search_steps=search_steps, num_of_individuals=num_of_individuals,  #每个iteration保留多少plan
                    # new_plans_num=new_plans_num,  #每一个plan0生成多少个新plan   ,batch_size=10
                    #coverage_increment_max=coverage_increment_max, search_cost_increment_max=search_cost_increment_max,  #plans_num_per=plans_num_per,
                    fig_path=fig_path)

    evo.evolve()

    end=time.time()
    with open(os.path.join(fig_path, "time.txt"), "w") as tf:
        tf.write(str(end-start))
    #print("execution time: "+ str(end-start))